from phe import paillier, EncryptedNumber
import random
import numpy as np


class PaillierEncryptor(object):
    """
    homomorphic encryption - Paillier scheme
    """
    def __init__(self):
        # generate random seed
        self.random_factor = random.randint(1, 999999)
        self.raw_public_key, self.private_key = paillier.generate_paillier_keypair(n_length=512)
        self.public_key = self.raw_public_key.encrypt(self.random_factor)

    def encrypt(self, plaintext):
        """
        Convert plaintext to ciphertext
        :param plaintext: numerical value(int, float, double...), numpy.Array, ...
        :return: ciphertext
        """
        return plaintext * self.public_key

    def decrypt(self, ciphertext):
        """
        Convert ciphertext to plaintext
        :param ciphertext:
        :return:
        """
        if isinstance(ciphertext, EncryptedNumber):
            plaintext = self.private_key.decrypt(ciphertext) / self.random_factor
            return plaintext

        if len(ciphertext.shape) == 2:
            plaintext = np.array([self._decrypt_vector(vec) for vec in ciphertext])
        else:
            plaintext = self._decrypt_vector(ciphertext)
        return plaintext

    def _decrypt_vector(self, ciphertext):
        plaintext = np.array([self.private_key.decrypt(num) for num in ciphertext]) / self.random_factor
        return plaintext

    def set_public_key(self, public_key):
        self.public_key = public_key
        self.random_factor = None
        self.raw_public_key = None
        self.private_key = None

    def get_public_key(self):
        return self.public_key
