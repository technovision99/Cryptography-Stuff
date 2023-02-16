import requests
flag_url = "https://aes.cryptohack.org/symmetry/encrypt_flag/"
encrypt_url = "https://aes.cryptohack.org/symmetry/encrypt/"


def bytes_xor(ba1, ba2):  
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def solve():
    r = requests.get(flag_url)
    ct = r.json()["ciphertext"]
    iv = ct[:32]
    ct = ct[32:]
    
    zero_string = "0" * len(ct)
    n = requests.get(encrypt_url + zero_string +"/"+iv+"/")
    encrypted_iv = n.json()["ciphertext"]
    print(encrypted_iv)
    print(ct)
    ct_bytes = bytearray.fromhex(ct)
    
    iv_bytes = bytearray.fromhex(encrypted_iv)
    print(len(ct_bytes))
    print(len(iv_bytes))
    pt = bytes_xor(ct_bytes,iv_bytes)
    print(pt.decode("ASCII"))
    
solve()
