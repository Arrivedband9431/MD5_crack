import socket
import threading


HOST = '0.0.0.0'
PORT = 65432
target_hash = "EC9C0F7EDCC18A98B1F31853B1813301".strip().lower()

# target_hash = "e665866de8ec4a64139aaa1d6ef85206"
# 3735928559 is the correct number
done = False
solution = None
work_load_size = 10000
current_min = 3730000000#1
lock = threading.Lock()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"started server port: {PORT} ")
    while not done:
        try:
            client, addr = server.accept()
            if done:
                client.sendall(b"done")
                client.close()
                break
            client_thread = threading.Thread(target=handle_client, args=(client,))
            client_thread.start()
        except KeyboardInterrupt:
            break



def handle_client(c_socket):
    global current_min, done, solution
    try:
        while not done:
            with lock:
                start_range = current_min
                current_min += work_load_size

            message = f"{target_hash},{start_range},{work_load_size}"
            c_socket.sendall(message.encode('utf-8'))
            response = c_socket.recv(1024).decode('utf-8')
            if not response:
                break

            if response.startswith("DONE:"):
                with lock:
                    done = True
                    solution = response.split(":")[1]
                c_socket.sendall(b"STOP")
                break
            elif response == "NOT_DONE":
                print("moving on")
                if done:
                    c_socket.sendall(b"STOP")
                    break
                continue
            elif response == "ALREADY_DONE":
                print("DONE")
                break

            if done and not solution:
                c_socket.sendall(b"STOP")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        c_socket.close()




if __name__ == '__main__':
    start_server()
