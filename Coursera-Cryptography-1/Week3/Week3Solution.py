from Crypto.Hash import SHA256

def solve(file):
    chunks = []
    with open(file,'rb') as f:
        while True:
            blocks = f.read(1024)
            chunks.append(blocks)
            if len(blocks) < 1024:
                break

    chunks = compute_hashes(chunks)
    print(chunks[0])

def compute_hashes(chunks):
    switched = chunks[::-1]
    index = 1
    while index <= len(switched)-1:
        h = SHA256.new(data=switched[index-1])
        switched[index] +=h.digest()
        index+=1

    h = SHA256.new(data=switched[len(switched)-1]).digest()
    switched.append(h)
    return [chunk.hex() for chunk in switched[::-1]]

#use path to downloaded file
solve("target.mp4")

