#Simple script to solve Question 1

def bytes_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

ct =  ["20814804c1767293b99f1d9cab3bc3e7","ac1e37bfb15599e5f40eef805488281d"]

iv = bytes.fromhex(ct[0])
padding1 = bytes("Pay Bob 100$","ASCII").ljust(16,b'0')
padding2 = bytes("Pay Bob 500$","ASCII").ljust(16,b'0')
u = bytes_xor(padding1,padding2)
res = bytes_xor(iv,u)
print(res.hex())