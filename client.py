import socket
import hashlib
import logging
ip = "127.0.0.1" #im running this locally so no need to change to my ip address
SERVER_PORT = 65432

logging.basicConfig(
    filename='client.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def crack(target,min_r,size):
    max_r = min_r+size
    for i in range(min_r,max_r):
        guess = str(i).encode("utf-8")
        guess_hash = hashlib.md5(guess).hexdigest()
        if guess_hash == target:
            print(f"the number was is {i}")
            logging.info(f"the number was is {i}")
            return i
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
            try:
                response = client.recv(1024).decode('utf-8')
            except socket.timeout:
                continue

            if not response or response == "STOP" or "done" in response:
                break
            target_hash, start_range, batch_size = response.split(",")
            start_range = int(start_range)
            batch_size = int(batch_size)
            result = crack(target_hash, start_range, batch_size)
            if result is not None:
                client.sendall(f"DONE:{result}".encode('utf-8'))
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