import hashlib

def sha256sum(filename):
    """Returns sha256sum for file"""

    f = file(filename, 'rb')
    m = hashlib.sha256()
    while True:
        b = f.read(8096)
        if not b:
            break
        m.update(b)
    f.close()
    return m.hexdigest()
