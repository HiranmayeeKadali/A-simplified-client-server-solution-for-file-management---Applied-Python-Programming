"""Testing Each Command"""
from pathlib import Path
import unittest
import os
import server

client = 'client'
passwd = 'passwd'
info = {
    'client': ''
}


def rm_tree(pth):
    """Removes recursively"""
    if pth.is_file():
        return pth.unlink()

    for child in pth.glob('*'):
        rm_tree(child)

    pth.rmdir()


class CommandTester(unittest.TestCase):
    """Testing Each Command"""

    def test_s1_register_or_login(self):
        """Test Login, Register"""
        server.register(info, f'{client} {passwd}')
        self.assertEqual(server.login(
            info, f'{client} {passwd}'), f'Logged In as {client}')
        self.assertNotEqual(info['client'], '')

    def test_s2_create_folder(self):
        """Test Create Folder"""
        server.create_folder(info, 'test_folder')
        self.assertTrue(Path(f'./client_dirs/{client}/test_folder').exists())

    def test_s3_file_creation_and_writing(self):
        """Test write file"""
        file = Path(f'./client_dirs/{client}/bla.txt')
        if file.exists():
            rm_tree(file)
        server.write_file(info, 'bla.txt Bla')
        self.assertTrue(file.exists())
        self.assertEqual(file.read_text(), 'Bla')

    def test_s4_read_file(self):
        """Test Read File"""
        return_value = server.read_file(info, 'bla.txt')
        text = Path(f'./client_dirs/{client}/bla.txt').read_text()
        self.assertEqual(text, return_value)

    def test_s5_list(self):
        """Test Listing Step"""
        return_value = server.lst(info)
        self.assertEqual(return_value, str(
            os.listdir(f'./client_dirs/{client}')))


if __name__ == '__main__':
    unittest.main()
