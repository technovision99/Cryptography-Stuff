import requests



def bytes_xor(ba1, ba2):  
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def split_into_blocks(text):
    blocks = [text[i:i+32] for i in range(0,len(text),32)]
    return blocks

def solve():
    decrypt_url = 'http://aes.cryptohack.org/ecbcbcwtf/decrypt/'
    encrypt_url = 'http://aes.cryptohack.org/ecbcbcwtf/encrypt_flag/'
    r = requests.get(encrypt_url)
    ciphertext = r.json()["ciphertext"]
    blocks = split_into_blocks(ciphertext)
    iv = blocks[0]
    blocks.remove(iv)
    to_xor = iv
    flag =""
    for block in blocks:
        print(block)
        r = requests.get(decrypt_url+block+"/")
        decrypted = r.json()["plaintext"]
        flag += bytes_xor(bytes.fromhex(decrypted),bytes.fromhex(to_xor)).decode("ASCII")
        to_xor = block
    print(flag)       


solve()
