import os
import tarfile
import json
import yaml
import tkinter as tk
import traceback
from datetime import datetime
from tkinter import scrolledtext


class ShellEmulator:
    def __init__(self, config_path):
        self.load_config(config_path)
        self.current_directory = '/'
        self.load_virtual_file_system()
        self.commands = {
            'ls': self.ls,
            'cd': self.cd,
            'exit': self.exit_emulator,
            'rmdir': self.rmdir,
            'mkdir': self.mkdir,
            'tac': self.tac
        }
        self.log_data = []

    def load_config(self, config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            self.hostname = config['hostname']
            self.vfs_path = config['vfs_path']
            self.log_path = config['log_path']

    def load_virtual_file_system(self):
        with tarfile.open(self.vfs_path) as tar:
            tar.extractall(path=self.get_tmp_directory())

    def get_tmp_directory(self):
        return 'tmp'

    def write_log(self):
        with open(self.log_path, 'w') as log_file:
            json.dump(self.log_data, log_file, indent=4)

    def execute_command(self, command):
        command = command.strip()
        if not command:
            return "Ошибка: команда не распознана"
        command_parts = command.split()
        cmd = command_parts[0]
        args = command_parts[1:]

        if cmd in self.commands:
            try:
                result = self.commands[cmd](*args)
                self.log_data.append({
                    "timestamp": datetime.now().isoformat(),
                    "command": command,
                    "result": result
                })
                self.write_log()
                return result
            except Exception as e:
                return f"Ошибка: {str(e)}"
        else:
            return "Ошибка: команда не распознана"

    def ls(self):
        path = os.path.join(self.get_tmp_directory(), self.current_directory.strip('/'))
        if os.path.exists(path):
            entries = os.listdir(path)
            return '\n'.join(entries) if entries else "Пустая директория"
        else:
            return "Ошибка: директория не найдена"

    def cd(self, path):
        if path == "..":
            self.current_directory = os.path.dirname(self.current_directory.rstrip('/'))
            if not self.current_directory:
                self.current_directory = '/'
        else:
            new_directory = os.path.join(self.current_directory, path)
            full_path = os.path.join(self.get_tmp_directory(), new_directory.strip('/'))
            if os.path.isdir(full_path):
                self.current_directory = new_directory
            else:
                return "Ошибка: директория не найдена"

    def exit_emulator(self):
        self.root.quit()

    def rmdir(self, path):
        full_path = os.path.join(self.get_tmp_directory(), self.current_directory.strip('/'), path)
        try:
            os.rmdir(full_path)
            return f"Удалена директория: {path}"
        except OSError:
            return "Ошибка: директория не пуста или не найдена"

    def mkdir(self, path):
        full_path = os.path.join(self.get_tmp_directory(), self.current_directory.strip('/'), path)
        try:
            os.mkdir(full_path)
            return f"Создана директория: {path}"
        except Exception as e:
            return f"Ошибка: {str(e)}"

    def tac(self, filename):
        full_path = os.path.join(self.get_tmp_directory(), self.current_directory.strip('/'), filename)

        try:
            with open(full_path, 'r') as file:
                return ''.join(reversed(file.readlines()))
        except Exception as e:
            return f"Ошибка: {str(e)}"

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title(f"Эмулятор оболочки - {self.hostname}")

        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.command_entry = tk.Entry(self.root)
        self.command_entry.pack(padx=10, pady=10, fill=tk.X)
        self.command_entry.bind("<Return>", self.process_command)

        self.root.mainloop()

    def process_command(self, event):
        command = self.command_entry.get()
        self.command_entry.delete(0, tk.END)
        result = self.execute_command(command)
        self.text_area.insert(tk.END, f"{self.hostname}: {command}\n{result}\n")
        self.text_area.see(tk.END)


if __name__ == '__main__':
    emulator = ShellEmulator('config.yaml')
    emulator.create_gui()

