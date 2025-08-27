def generate(length: int,characterSet: str = None) -> str:
    """
    Generates a random text using the given character set.

    Params:
        characterSet: The set from which the characters will be selected for the password.
        length: The length of password to be generated.

    Returns:
        A string of the generated password.

    Example:
        generate("abcdefghijklmnopqrstuvwxyz",20)
    """
    import secrets
    password = ['']*length

    if characterSet == None:
        import string
        characterSet = string.ascii_letters+string.digits+string.punctuation

    for i in range(length):
        password[i] = secrets.choice(characterSet)

    return "".join(password)

def generateCustom(textInput: str, length: int) -> str:
    """
    Generates a random text using a simplified character markdown.
    
    Params:
        textInput: Custom characterset input using the markdown.
        length: The length of the password to be generated.

    Returns:
        A string of the generated password.

    Example:
        generateCustom("a-zA-Z0-9\\\\-?!%/*+-",30)
    """
    import re
    characterSet = ""
    regexText = r"\\([\\-])|(.)-(.)|(.)"
    for match in re.findall(regexText,textInput):
        if match[0]:
            characterSet += match[0]
        elif match[3]:
            characterSet += match[3]
        else:
            for i in range(ord(match[1]),ord(match[2])):
                characterSet += chr(i)
    
    return generate(length,characterSet)
