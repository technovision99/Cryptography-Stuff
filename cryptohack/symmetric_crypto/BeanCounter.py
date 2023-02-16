import requests

encrypt_url = "http://aes.cryptohack.org/bean_counter/encrypt/"
# Every png file starts with this header
PNG_PREFIX = bytes([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0x00, 0x00, 0x00, 0x0d, 0x49, 0x48, 0x44, 0x52])

def bytes_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def solve():
    ct = bytes.fromhex(requests.get(encrypt_url).json()["encrypted"])
    iv = bytes_xor(ct[:16],PNG_PREFIX)

    blocks = [ct[i:i+16] for i in range(16,len(ct),16)]
    png_dump=PNG_PREFIX
    for block in blocks:
        png_dump +=(bytes_xor(block,iv))

    with open("decrypted.png","wb") as fi:
        fi.write(png_dump)






solve()
