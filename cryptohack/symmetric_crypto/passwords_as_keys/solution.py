from Crypto.Cipher import AES
import hashlib


def decrypt(ciphertext, password_hash):
    ciphertext = bytes.fromhex(ciphertext)
    key = bytes.fromhex(password_hash)

    cipher = AES.new(key, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
    except ValueError as e:
        return {"error": str(e)}
    
    return {"plaintext": decrypted.hex()}

with open("words.txt") as f:
    words = [w.strip() for w in f.readlines()]

for word in words:
    KEY = hashlib.md5(word.encode()).digest().hex()
    plaintext = decrypt("c92b7734070205bdf6c0087a751466ec13ae15e6f1bcdd3f3a535ec0f4bbae66",KEY)
    plaintext_val = plaintext.get("plaintext")
    try:
        decoded = bytearray.fromhex(plaintext_val).decode("ASCII")
        if "crypto" in decoded:
            print(KEY)
            print(decoded)
            break 
    except:
        continue
