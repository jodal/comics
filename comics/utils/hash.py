import hashlib

def sha256sum(filename=None, filehandle=None):
    """Returns sha256sum for file"""

    if filename is not None:
        f = file(filename, 'rb')
    else:
        f = filehandle
        original_position = f.tell()
    m = hashlib.sha256()
    while True:
        b = f.read(8096)
        if not b:
            break
        m.update(b)
    if filename is not None:
        f.close()
    else:
        f.seek(original_position)
    return m.hexdigest()
