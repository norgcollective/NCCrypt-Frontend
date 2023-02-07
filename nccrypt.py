# Version 1.0
# NCCrypt is NOT backward-compatible
# NCCrypt-Version: 1.1

from hashlib import sha1
from nclib import AddAndReset, SubAndReset


def encrypt(unencrypted, passwd=""):

    # Lets make sure that the unencrypted data is a string
    unencrypted = str(unencrypted)
    # Unencrypted data is now a string

    encrypted = ""

    # Lets make the Password usable
    if passwd is None:
        passwd=""
    passwd = str(passwd)
    passwd = sha1(passwd.encode('utf-8')).hexdigest()

    while len(passwd) < len(unencrypted):
        passwd += passwd

    while len(unencrypted) < len(passwd):
        unencrypted += " "
    # Password is now usable

    # Lets create Variables
    decrypted = ""
    cache     = ""
    # Variables created

    # Lets encrypt
    for i in range(len(unencrypted)):
        encrypted += chr( AddAndReset(0,128, ord(unencrypted[i]), ord(passwd[i])) )

    cache = encrypted
    encrypted = ""

    for i in range(len(cache)):
        encrypted += chr( AddAndReset(0,128, ord(cache[i]), AddAndReset(0,128,0,i) ) )
    # String encrypted

    return encrypted

def decrypt(encrypted, passwd=""):

    unencrypted = ""

    # Lets make sure that the unencrypted data is a string
    unencrypted = str(unencrypted)
    # Unencrypted data is now a string

    # Lets make the Password usable
    if passwd is None:
        passwd = ""
    passwd = str(passwd)
    passwd = sha1(passwd.encode('utf-8')).hexdigest()
    #Password is now usable

    # Lets make sure the password is long enough
    while len(passwd) < len(encrypted):
        passwd += passwd

    # Lets create Variables
    decrypted = ""
    cache     = ""
    # Variables created

    # Lets decrypt
    for i in range(len(encrypted)):
        decrypted += chr( SubAndReset(0,128, ord(encrypted[i]), AddAndReset(0,128,0,i)) )

    cache = decrypted
    decrypted = ""

    for i in range(len(cache)):
        decrypted += chr( SubAndReset(0,128, ord(cache[i]), ord(passwd[i])) )

    return decrypted.strip()
