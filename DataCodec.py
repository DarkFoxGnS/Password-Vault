import hashlib
import hmac

DEFSALT = "b2e753fe8a9c9aebd5fa299d9ee6f07d319f8e1b110cfcf1cd77daae00c8e83825076e46bb5255c501cfec7adf1923d0745ab09e48a1ed74c5817e699225cdd83"

def hmac_salt (password: bytes, salt: bytes) -> bytes:
    """
    Creates an hmac encoded hash.
    
    Params:
        password: The password as a byte array.
        salt: The salt to be encoded.

    Returns:
        Returns a byte array of encoded data.
    """
    return hmac.new(password,salt, hashlib.sha256).digest()


def argon2_hash(key: bytes, salt: bytes, hash_len=64) -> bytes:
    """
    Hashes using argon2.
    
    Params:
        password: The password as a byte array.
        salt: The salt as a byte array.
        hash_len: The length of the return hash

    Returns:
        Byte array of the hash.
    """
    from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
    return Argon2id(
        salt = salt,
        length = 64,
        iterations = 10,
        lanes = 2,
        memory_cost = 52428
    ).derive(key)

def generate_CSPRNG(seed: bytes):
    """
    Generates a 64 byte long hash based pseudo-random byte sequence.

    Params:
        seed: Byte array of seed

    Returns:
        64 byte long byte sequence.
    """
    return bytes((a+b)%256 for a,b in zip(hashlib.sha256(seed).digest()+hashlib.sha256(seed).digest(),hashlib.sha512(seed).digest()))

def make_password(password1: bytes, seed: bytes) -> bytes:
    """
    Generates the encryption password.
        
    Params:
        password1: Byte array of password.
        seed: Byte array of seed.
        length: The amound of passwords to generate. A length of 1 generates a 64 byte passwords.

    Returns:
        A byte array of password.
    """
    
    salt = generate_CSPRNG(seed)

    return argon2_hash(password1,hmac_salt(password1,salt)),salt

def encode(password1: bytes, password2: bytes, secret: bytes) -> bytes:
    """
    Encodes the secret using the password.
    
    Params:
        password1: A byte array of the password.
        password2: A byte array of the password (basis of salt). Can be None.
        secret: A byte array of the text to be encoded.

    Returns:
        Byte array containing the encoded data.
    """
    
    if password2 == None:
        password2 = DEFSALT

    password1 = password1.encode()
    password2 = password2.encode()
    if not isinstance(secret,bytes):
        raise Exception("The secret must be bytes.")
    
    encoded = [0]*len(secret)
    password, seed = make_password(password1, password2)
    for i in range(len(secret)):
        if i % len(password) == 0:
            password,seed = make_password(password,seed)
        encoded[i] = (secret[i]+password[i%len(password)])%256
    
    return bytes(encoded)

def decode(password1: bytes, password2: bytes, secret: bytes) -> str:
    """
    Decodes the secret using the provided password.
    
    Params:
        password1: A byte array of the password.
        password1: A byte array of the password (basis of salt). Can be None.
        secret: A byte array representation of the secret.

    Returns:
        The decoded byte array.
    """
    if password2 == None:
        password2 = DEFSALT

    password1 = password1.encode()
    password2 = password2.encode()

    if not isinstance(secret,bytes):
        print("The secret must be the type of bytes.")

    decoded = [0]*len(secret)
    password, seed = make_password(password1, password2)
    
    zeros = 0

    for i in range(len(secret)):
        if i % len(password) == 0:
            password,seed = make_password(password,seed)

        decoded[i] = (secret[i]-password[i%len(password)])%256
        if decoded[i] == 0:
            zeros+=1
            if zeros == 3:
                return bytes(decoded[:i+1])
        else:
            zeros = 0
    
    return bytes(decoded)
