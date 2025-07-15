# Password Vault

## Disclaimer!
The software is work in progress.

## Encryption method:
    The software uses a per byte encryption method similar to Vigenére cipher, with the difference being a nearly infinite generated pseudorandom password as key.

## Key generation:
    The is at least as long as the content to be encoded. The key is generated via Argon2 hashing algorithm, which is uses the main password salted with a HMAC.

## Data storage:
    The data is stored using Steganography in multiple images. Images that are incorrects are filled in with fake data.
