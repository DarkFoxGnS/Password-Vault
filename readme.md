# Password Vault

## Disclaimer!
__The software is work in progress!__

###ToDo:
- Load File
  - User Interface
    - Landing page
    - Loader page (if needed)
  - Functionality
    - Load file
    - Decrypt file (using user input)
- New File
  - User Interface
    - Landing page
    - Loader page (if needed)
  - Functionality
    - Make new file
    - Encrypt file
  - Unit testing
- Manage existing file
  - User Interface
    - Password listing
    - Addition of new password
  - Functionality
    - Allow the users to generate a new password according to their needs in format.
    - Save this password to the file
    - Create fake/bait files.
  - Unit testing


## Encryption method:
The software uses a per byte encryption method similar to Vigenére cipher, with the difference being a nearly infinite generated pseudorandom password as key.

## Key generation:
The is at least as long as the content to be encoded. The key is generated via Argon2 hashing algorithm, which is uses the main password salted with a HMAC.

## Data storage:
The data is stored using Steganography in multiple images. Images that are incorrects are filled in with fake data.
