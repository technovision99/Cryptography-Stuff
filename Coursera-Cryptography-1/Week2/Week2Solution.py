from AES import AES
import os 
import random


def bytes_xor(ba1, ba2):  
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def pad_bytes(text):
    xs = bytearray(text)
    length = len(text) % 16 
    xs += (bytes([16-length])*(16-length))
    return bytes(xs)

def split_into_blocks(text):
    blocks = [text[i:i+16] for i in range(0,len(text),16)]
    return blocks
    
def AES_CBC_encrypt(plaintext, key,iv):
    padded = pad_bytes(plaintext)
    blocks = split_into_blocks(padded)
    aes = AES(key) 
    current_block = bytes_xor(blocks[0],iv)
    ciphertext = bytearray(iv)
    for block in blocks:
        if block == blocks[0]:
            current_block = aes.encrypt_block(current_block)
            ciphertext += current_block
        else:
            current_block = aes.encrypt_block(bytes_xor(current_block,block))
            ciphertext += current_block
        
    return ciphertext

# assumes IV is prepended to ciphertext
def AES_CBC_decrypt(ciphertext,key):
    aes = AES(key)
    plaintext = bytearray()
    blocks = split_into_blocks(ciphertext)
    iv = strip_iv(ciphertext)
    blocks.remove(iv)
    to_xor = iv
    for block in blocks:
        decrpyted = aes.decrypt_block(block)
        plaintext += bytes_xor(decrpyted,to_xor)
        to_xor = block
    padding_to_remove = int.from_bytes(plaintext[-1:],"big")
    plaintext = plaintext [:-padding_to_remove]
    return plaintext

def byte_length(i):
    return (i.bit_length() + 7) // 8

def strip_iv(block):
    return block[0:16]


def AES_CTR_encrypt(plaintext, key, iv):
    blocks = split_into_blocks(plaintext)
    ciphertext = bytearray(iv)
    aes = AES(key)
    for i in range(0,len(blocks)):
        incremented = int.from_bytes(iv,"big")+i
        ciphertext += bytes_xor(blocks[i],aes.encrypt_block((incremented.to_bytes(byte_length(incremented),"big"))))
    return ciphertext

# assumes IV is prepended to ciphertext
def AES_CTR_decrypt(ciphertext,key):
    aes = AES(key)
    iv = strip_iv(ciphertext)
    plaintext = bytearray()
    blocks = split_into_blocks(ciphertext)
    blocks.remove(iv)
    for i in range(0,len(blocks)):
        incremented = int.from_bytes(iv,"big")+i
        plaintext += bytes_xor(blocks[i],aes.encrypt_block((incremented.to_bytes(byte_length(incremented),"big"))))
    
    return plaintext


cbc_key_1 = bytes.fromhex("140b41b22a29beb4061bda66b6747e14")
cbc_ciphertext_1 = bytes.fromhex("4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81")
decryption_1 = AES_CBC_decrypt(cbc_ciphertext_1,cbc_key_1)
cbc_key_2 = bytes.fromhex("140b41b22a29beb4061bda66b6747e14")
cbc_ciphertext_2 = bytes.fromhex("5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253")
decryption_2 = AES_CBC_decrypt(cbc_ciphertext_2,cbc_key_2)
print(decryption_1.decode("ASCII"))
print(decryption_2.decode("ASCII"))
ctr_key_1 = bytes.fromhex("36f18357be4dbd77f050515c73fcf9f2")
ctr_key_2 = bytes.fromhex("36f18357be4dbd77f050515c73fcf9f2")
ctr_ciphertext_1 = bytes.fromhex("69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329")
ctr_ciphertext_2 = bytes.fromhex("770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451")
ctr_decryption_1 = AES_CTR_decrypt(ctr_ciphertext_1,ctr_key_1)
ctr_decryption_2 = AES_CTR_decrypt(ctr_ciphertext_2,ctr_key_2)
print(ctr_decryption_1.decode("ASCII"))
print(ctr_decryption_2.decode("ASCII"))

#ciphertext1 = AES_CTR_decrypt(AES_CTR_encrypt(test,key,iv),key)
#ciphertext2 = aes.decrypt_ctr(aes.encrypt_ctr(test,iv),iv)
#print(ciphertext1.hex())
#print(ciphertext2.hex())








