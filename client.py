import socket
import hashlib
import logging
import threading
import time

ip = "127.0.0.1" #im running this locally so no need to change to my ip address
SERVER_PORT = 65432
max_threads = 5
max_thread = threading.BoundedSemaphore(max_threads)
found_event = threading.Event()




logging.basicConfig(
    filename='client.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
def thread_creator():
    therads = []
    for i in range(max_threads):
        t = threading.Thread(target=start_client)
        t.start()
        therads.append(t)
        time.sleep(0.1)


def crack(target,min_r,size):
    global max_thread
    with max_thread:
        max_r = min_r +size
        for j in range(min_r,max_r):
            if found_event.is_set():
                return None
            guess = str(j).encode("utf-8")
            guess_hash = hashlib.md5(guess).hexdigest()
            if guess_hash == target:
                print(f"the number was is {j}")
                logging.info(f"the number was is {j}")
                found_event.set()
                return j
    return None


def start_client():
    client = None

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, SERVER_PORT))
        print("connected")
        logging.info("connected")
        client.settimeout(2.0)
        while True:

            if found_event.is_set():
                break

            try:
                response = client.recv(1024).decode('utf-8')
            except socket.timeout:
                continue

            if not response or response == "STOP" or "done" in response:
                break

            target_hash, start_range, batch_size = response.split(",")
            start_range = int(start_range)
            batch_size = int(batch_size)

            chunk_size = batch_size // 5
            threads = []
            found_event.clear()
            print(start_range)
            for i in range(5):
                thread_start = start_range + (i * chunk_size)
                t = threading.Thread(target=crack, args=(target_hash, thread_start, chunk_size))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

            if found_event.is_set():
                client.sendall(b"DONE:")
                break
            else:
                client.sendall(b"NOT_DONE")

    except Exception as e:
        print(f"Error: {e}")
        logging.error(f"Error: {e}")

    finally:
        client.close()
        logging.warning("closing connection")

if __name__ == "__main__":
    start_client()