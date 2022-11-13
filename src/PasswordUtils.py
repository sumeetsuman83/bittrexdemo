from cryptography.fernet import Fernet
from decouple import config
# we will be encrypting the below string.

def EncryptPassword(message):
    key=open("../data/key.key", "rb").read()
    fernet = Fernet(key)
    encMessage = fernet.encrypt(message.encode())
    return encMessage

    # print("original string: ", message)
    # print("encrypted string: ", encMessage)

    # # decrypt the encrypted string with the
    # # Fernet instance of the key,
    # # that was used for encrypting the string
    # # encoded byte string is returned by decrypt method,
    # # so decode it to string with decode methods
    # decMessage = fernet.decrypt(encMessage).decode()

    # print("decrypted string: ", decMessage)

# gAAAAABjcQ-J8Gzkq8a2oqQMwZuEpcrddqnVBpyHzFKUAppq4gNRU3hf65Zw1nHnouNjZCHdtbV-paD6X34Uj-ki6Wiif4DGGA==



def DecryptPassword(password):
    key=open("../data/key.key", "rb").read()
    fernet = Fernet(key)
    decMessage = fernet.decrypt(password).decode()
    return decMessage



if __name__ == "__main__":
    s=b"gAAAAABjcST0_LXLidT55TCzoSeIwR1oQbKBzRNoV9p_wba1ScUBq9RP7SxBCj_fo5tNaymxL-80krrwGmBFgwKTM3SXgcy6IA=="
    print(type(s))
    name=DecryptPassword(s)
    print(name)