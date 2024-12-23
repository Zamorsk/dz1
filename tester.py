import unittest
import os

from ShellEmulator import ShellEmulator


class TestShellEmulator(unittest.TestCase):

    def setUp(self):
        self.emulator = ShellEmulator('config.yaml')

    def test_ls(self):
        # Проверяем, что список файлов корректен
        expected_output = os.listdir(self.emulator.get_tmp_directory())
        result = self.emulator.ls()
        self.assertEqual(result.splitlines(), expected_output)

    def test_cd(self):
        # Проверяем смену директории
        self.emulator.mkdir('new_dir')
        self.emulator.cd('new_dir')
        self.assertEqual(self.emulator.current_directory, '/new_dir')

    def test_mkdir(self):
        # Проверяем создание директории
        result = self.emulator.mkdir('test_dir')
        self.assertIn('Создана директория', result)

    def test_rmdir(self):
        # Проверяем удаление директории
        self.emulator.mkdir('temp_dir')
        result = self.emulator.rmdir('temp_dir')
        self.assertIn('Удалена директория', result)

    def test_tac(self):
        # Проверяем команду tac
        test_file = os.path.join(self.emulator.get_tmp_directory(), 'test_file.txt')
        with open(test_file, 'w') as f:
            f.write('line1\nline2\nline3\n')

        result = self.emulator.tac('test_file.txt')
        self.assertEqual(result, 'line3\nline2\nline1\n')


if __name__ == '__main__':
    unittest.main()
