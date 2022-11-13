import requests

get_cookie_url = "http://aes.cryptohack.org/flipping_cookie/get_cookie/"
check_flag_url = "http://aes.cryptohack.org/flipping_cookie/check_admin/"


def bytes_xor(ba1, ba2):  
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def solve():
    r = requests.get(get_cookie_url)
    ciphertext = r.json()["cookie"]
    iv = ciphertext[0:32]
    cookie = ciphertext[32:]
    false_string = str.encode("admin=False;")
    true_string = str.encode("admin=True;") 
    xord = bytes_xor(false_string,true_string)
    new_iv = bytes_xor(xord,bytes.fromhex(iv)).hex()
    print(len(new_iv)) # this has length 22, we need to pad to get 16 byte IV
    
   
    try:
        r = requests.get(check_flag_url+cookie+'/'+new_iv+'0000000000'+'/')
        flag = r.json()["flag"]
        print(flag)
    except:
        print("failed")
    

solve()

