import hashlib
from argon2 import low_level
import hmac

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


def argon2_hash(password: bytes, salt: bytes, hash_len=64) -> bytes:
    """
    Hashes using argon2.
    
    Params:
        password: The password as a byte array.
        salt: The salt as a byte array.
        hash_len: The length of the return hash

    Returns:
        Byte array of the hash.
    """
    return low_level.hash_secret_raw(
        secret = password,
        salt = salt,
        time_cost=3,
        memory_cost = 65536,
        parallelism = 2,
        hash_len = hash_len,
        type = low_level.Type.ID
        )

def make_password(password_bytes: bytes,length: int) -> bytes:
    """
    Generates the encryption password.
        
    Params:
        password_bytes: Byte array of password.
        length: The amound of passwords to generate. A length of 1 generates a 64 byte passwords.

    Returns:
        A byte array of password.
    """

    encrypt_key = b""
    print("Generating key:")
    for i in range(length):
        key = argon2_hash(password_bytes,hmac_salt(password_bytes,bytes(f"salt{i}","UTF-8")))
        print(f"\tAppending key[{len(key)}]: ",key.hex())
        encrypt_key+=key
    print(f"Using Encryption Key[{len(encrypt_key)}]: ",encrypt_key.hex())
    return encrypt_key

def encode(password: bytes, secret: bytes) -> "(bytes, str of hex)":
    """
    Encodes the secret using the password.
    
    Params:
        password: A byte array of the password.
        secret: A byte array of the text to be encoded.

    Returns:
        A tuple of the encoded bytes and the hex representation of the bytes.
    """

    if not isinstance(password,bytes):
        raise Exception("The password must be bytes.")
    if not isinstance(secret,bytes):
        raise Exception("The secret must be bytes.")

   # Create enough keys to encode the text.
    encrypt_key = make_password(password, len(secret)//64+1)
    
    # Mod encode the text
    encoded = bytes((x+y)%256 for x,y in zip(secret,encrypt_key))
    
    return encoded, encoded.hex()

def decode_hex(input_text: str) -> bytes:
    """
    Decodes the hex string into a byte array.
    
    Params:
        input_text: Hex string to be decoded.

    Returns:
        Decoded byte array.
    """
    combined = b"" 
    for i in range(len(input_text)//2):
        combined += int(input_text[i*2:i*2+2],16).to_bytes()
    
    return combined

def decode(password: bytes, secret: "string of hex or bytes") -> str:
    """
    Decodes the secret using the provided password.
    
    Params:
        password: A byte array of the password.
        secret: A string or byte array representation of the secret.

    Returns:
        The decoded byte array.
    """
    if not isinstance(password, bytes):
        print("The password must be the type of bytes.")
    if not isinstance(secret,(bytes,str)):
        print("The secret must be either a string of hex or bytes.")

    # If string of hex is presented convert into binary data
    if type(secret) == str:
        secret = decode_hex(secret)

    # Create enough keys to decode the text.
    encrypt_key = make_password(password, len(secret)//64+1)
    
    # Mode decode the text
    decoded = bytes((x-y)%256 for x,y in zip(secret,encrypt_key))

    return decoded

if __name__ == "__main__":
    match(input("(E)ncode or (D)ecode: ")):
        case "E" | "e":
            password = input("Enter a password: ")
            secret = input("Enter a text to be encoded: ")
            res = encode(password.encode(),secret.encode())
            print(res)
        case "D" | "d":
            password = input("Enter a password: ")
            secret = input("Enter a secret text to be decoded: ")
            res = decode(password.encode(), secret)
            print(res.decode())
