import requests
import string
import time
alphabet = '_'+'@'+'}'+'{'+string.digits+string.ascii_lowercase+string.ascii_uppercase


def print_blocks(str,sz):
    for i in range(0,len(str),sz):
        print(str[i:i+sz]+" ",end ='')
    print()

def encrypt(payload):
    url = "http://aes.cryptohack.org/ecb_oracle/encrypt/" + payload + "/"
    r = requests.get(url)
    return r.json()["ciphertext"]


def brute_force():
    flag = ""
    total = 31
    
    while True:
        padding = "1"*(total-len(flag))
        expected = encrypt(padding.encode().hex())
        print("E" + ' ', end='')
        print_blocks(expected,32)
        for c in alphabet:
            print((padding+flag+c).encode())
            returned = encrypt(bytes.hex((padding+flag+c).encode()))
            print(c+ " ",end='')
            print_blocks(returned,32)
            if returned[32:64] == expected[32:64]:
                flag+=c
                print(flag)
                break
        time.sleep(1)
        if flag.endswith("}"):
            break
    print(flag)
    
brute_force()


