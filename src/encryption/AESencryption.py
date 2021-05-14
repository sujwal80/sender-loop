from Crypto.Cipher import AES
import hashlib
from Crypto import Random
from base64 import b64decode, b64encode

class AEScipher(object):

    def __init__(self):
        self.blockSize = AES.block_size
        #Ujwal_Singh is taken as example for Private Key
        self.privateKey = hashlib.sha256("Ujwal_Singh".encode()).digest()


    def __padding(self, plainText):
        number_of_character_missing = self.blockSize - len(plainText) % self.blockSize
        asciiCharacter = chr(number_of_character_missing)
        padding = asciiCharacter * number_of_character_missing

        return plainText + padding


    def __unpadding(self, plainText):
        lastCharacter = plainText[len(plainText) -1:]
        toRemove = ord(lastCharacter)

        return plainText[:len(plainText) - toRemove]


    def encrypt(self, plainText):
        plainText = self.__padding(plainText)

        IV = Random.new().read(self.blockSize)

        cipher = AES.new(self.privateKey, AES.MODE_CBC, IV)

        encryptedText = cipher.encrypt(plainText)

        return b64encode(IV + encryptedText)


    def decrypt(self, encryptedText):
        encryptedText = b64decode(encryptedText)
        IV = encryptedText[:self.blockSize]

        cipher = AES.new(self.privateKey, AES.MODE_CBC, IV)

        plainText = cipher.decrypt(encryptedText[self.blockSize:])

        return self.__unpadding(plainText)