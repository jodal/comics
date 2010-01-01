import hashlib

def sha256sum(filename=None, filehandle=None):
    """Returns sha256sum for file"""

    if filename is not None:
        f = file(filename, 'rb')
    else:
        f = filehandle
    m = hashlib.sha256()
    while True:
        b = f.read(8096)
        if not b:
            break
        m.update(b)
    if filename is not None:
        f.close()
    return m.hexdigest()
