import unittest

import numpy as np

from encryptor.paillier_encryptor import PaillierEncryptor


class TestPaillierEncryptor(unittest.TestCase):
    def setUp(self):
        self.encryptor = PaillierEncryptor()

    def test(self):
        p = 1e-6

        # one-dimensional int np.array
        plaintext1 = np.array([1, 2, 3, 4, 5])
        ciphertext1 = self.encryptor.encrypt(plaintext1)
        dec_plaintext1 = self.encryptor.decrypt(ciphertext1)
        assert (plaintext1 - dec_plaintext1).sum() < p

        # one-dimensional float np.array
        plaintext2 = np.array([1.1, 2.2, 3.3, 4.4, 5.5])
        ciphertext2 = self.encryptor.encrypt(plaintext2)
        dec_plaintext2 = self.encryptor.decrypt(ciphertext2)
        assert (plaintext2 - dec_plaintext2).sum() < p

        # two-dimensional int np.array
        plaintext3 = np.array([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]])
        ciphertext3 = self.encryptor.encrypt(plaintext3)
        dec_plaintext3 = self.encryptor.decrypt(ciphertext3)
        assert (plaintext3 - dec_plaintext3).sum() < p

        # two-dimensional float np.array
        plaintext4 = np.array([[1.1, 2.2, 3.3, 4.4, 5.5], [1.1, 2.2, 3.3, 4.4, 5.5]])
        ciphertext4 = self.encryptor.encrypt(plaintext4)
        dec_plaintext4 = self.encryptor.decrypt(ciphertext4)
        assert (plaintext4 - dec_plaintext4).sum() < p

        # add: enc_x + enc_y
        plaintext5 = np.array([[1, 2, 3, 4, 5], [1.5, 2.5, 3.5, 4.5, 5.5]])
        plaintext6 = np.array([[10.5, 11.5, 12.5, 13.5, 14.5], [1.5, 2.5, 3.5, 4.5, 5.5]])
        enc_plaintext5 = self.encryptor.encrypt(plaintext5)
        enc_plaintext6 = self.encryptor.encrypt(plaintext6)

        enc_res = enc_plaintext5 + enc_plaintext6
        dec_res = self.encryptor.decrypt(enc_res)
        expect_res = np.array([[11.5, 13.5, 15.5, 17.5, 19.5], [3., 5., 7., 9., 11.]])
        assert (dec_res - expect_res).sum() < p

        # multiplication: enc_x * y
        plaintext7 = np.array([[1.5, 2.5, 3.5, 4.5, 5.5], [1.5, 2.5, 3.5, 4.5, 5.5]])
        enc_plaintext7 = self.encryptor.encrypt(plaintext7)
        enc_res = enc_plaintext7 * 2
        dec_res = self.encryptor.decrypt(enc_res)
        expect_res = np.array([[3., 5., 7., 9., 11.], [3., 5., 7., 9., 11.]])
        assert (dec_res - expect_res).sum() < p

        """
        1. A send public_key to B
        2. B set public_key
        3. B: compute ciphertext * 2
        4. A: decrypt
        """
        B = PaillierEncryptor()
        A_public_key = self.encryptor.get_public_key()
        B.set_public_key(A_public_key)

        plaintext8 = np.array([1.5, 1.5, 1.5, 2.5])
        ciphertext8 = B.encrypt(plaintext8)
        enc_res = ciphertext8 * 2
        dec_res = self.encryptor.decrypt(enc_res)
        expect_res = np.array([3., 3., 3., 5.])
        assert (dec_res == expect_res).all()


if __name__ == '__main__':
    unittest.main()
