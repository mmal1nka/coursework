import unittest

from coursework.Vigenere.vigenerecipher import encrypt, decrypt


class CipherTest(unittest.TestCase):
    def setUp(self):
        pass

    def test1(self):
        result = encrypt('I love TUSUR', 'key')
        self.assertEqual('SDIyzBJX&!Y#', result)

    def test2(self):
        result = decrypt('SDIyzBJX&!Y#', 'key')
        self.assertEqual('I love TUSUR', result)

    def test3(self):
        result = encrypt('How are you doing?', 'dog')
        self.assertEqual('KBBCoxhNDrHFgBoqu6', result)

    def test4(self):
        result = decrypt('KBBCoxhNDrHFgBoqu6', 'dog')
        self.assertEqual('How are you doing?', result)

    def test5(self):
        result = encrypt('', 'cat')
        self.assertEqual('', result)

    def test6(self):
        result = encrypt('7959834430567', 'number')
        self.assertEqual('+<^0#+^[&@9/+', result)

    def test7(self):
        result = decrypt('+<^0#+^[&@9/+', 'number')
        self.assertEqual('7959834430567', result)

    def test8(self):
        result = encrypt('Hello!', 'beautiful')
        self.assertEqual('', result)

    def test9(self):
        result = encrypt('Привет', 'да')
        self.assertEqual('', result)

    def test10(self):
        result = decrypt('Hello', 'да')
        self.assertEqual('', result)