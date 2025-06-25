import hashlib
from argon2 import low_level
import hmac

def hmac_salt (password: bytes, salt: bytes):
    return hmac.new(password,salt, hashlib.sha256).digest()

def argon2_hash(password: bytes, salt: bytes, hash_len=64):
    return low_level.hash_secret_raw(
        secret = password,
        salt = salt,
        time_cost=3,
        memory_cost = 65536,
        parallelism = 2,
        hash_len = hash_len,
        type = low_level.Type.ID
        )

def make_password(password_bytes: bytes,length: int):

    encrypt_key = b""
    print("Generating key:")
    for i in range(length):
        key = argon2_hash(password_bytes,hmac_salt(password_bytes,bytes(f"salt{i}","UTF-8")))
        print(f"\tAppending key[{len(key)}]: ",key.hex())
        encrypt_key+=key
    print(f"Using Encryption Key[{len(encrypt_key)}]: ",encrypt_key.hex())
    return encrypt_key

def encode():
    # Take user input 
    password = input("Enter a password: ")
    secret = input("Enter a text to be encoded: ")
   
   # Create enough keys to encode the text.
    encrypt_key = make_password(bytes(password,"UTF-8"), len(secret)//64+1)
    
    # Mod encode the text
    secret = secret.encode("UTF-8")
    encoded = bytes((x+y)%256 for x,y in zip(secret,encrypt_key))
    print(encoded)
    print(
            "\tPython Hex:",encoded,"\n",
            "\tHexadecimal:",encoded.hex(),"\n",
            "\tEncoded text size:",len(encoded)*8,"Bytes"
            )

def decode_hex(input_text):
    combined = b"" 
    for i in range(len(input_text)//2):
        combined += int(input_text[i*2:i*2+2],16).to_bytes()
    return combined

def decode():
    # Take user input
    password = input("Enter a password: ")
    secret = input("Enter the secret to be decoded: ")
    
    secret = decode_hex(secret)
    print(secret)

    # Create enough keys to decode the text.
    encrypt_key = make_password(bytes(password,"UTF-8"), len(secret)//64+1)
    
    # Mode decode the text
    decoded = bytes((x-y)%256 for x,y in zip(secret,encrypt_key))

    print(decoded.decode())

match(input("(E)ncode or (D)ecode: ")):
    case "E" | "e":
        encode()
    case "D" | "d":
        decode()
