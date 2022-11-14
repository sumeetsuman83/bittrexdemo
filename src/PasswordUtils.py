from cryptography.fernet import Fernet
from decouple import config
# we will be encrypting the below string.

def EncryptPassword(message):
    """
    The EncryptPassword function takes a string as an argument and returns the encrypted version of that string.
    It uses the Fernet encryption algorithm to encrypt the password, which is then returned.
    
    :param message: Encrypt the password
    :return: The encrypted message
    """
    key=open(config("passwordkey"), "rb").read()
    fernet = Fernet(key)
    encMessage = fernet.encrypt(message.encode())
    return encMessage


def DecryptPassword(password):
    """
    The DecryptPassword function takes a password and decrypts it using the Fernet encryption algorithm.
    It then returns the decrypted password.
    
    :param password: Decrypt the password
    :return: The decrypted password
    """
    key=open(config("passwordkey"), "rb").read()
    fernet = Fernet(key)
    decMessage = fernet.decrypt(password).decode()
    return decMessage



if __name__ == "__main__":
    s=b"gAAAAABjcST0_LXLidT55TCzoSeIwR1oQbKBzRNoV9p_wba1ScUBq9RP7SxBCj_fo5tNaymxL-80krrwGmBFgwKTM3SXgcy6IA=="
    print(type(s))
    name=DecryptPassword(s)
    print(name)