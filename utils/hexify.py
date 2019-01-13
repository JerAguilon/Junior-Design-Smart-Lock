def hexify(s):
    b = str.encode(s)
    return b.hex()

def dehexify(s):
    b = bytes.fromhex(s)
    return b.decode()
