import hashlib

#final_encrypted_text = "EC9C0F7EDCC18A98B1F31853B1813301 "

msg = "EC9C0F7EDCC18A98B1F31853B1813301"
work_load_size = 10000

def crack(target,min,size):
    max = min+size
    for i in range(min,max):
        guess = str(i).encode("utf-8")
        guess_hash = hashlib.md5(guess).hexdigest()
        if guess_hash == target:
            print(f"the number was is {i}")
            return True
    return None


if __name__ == "__main__":
    for i in range(1,10000):
        if crack(msg,i,work_load_size):
            break
