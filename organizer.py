from tkinter import messagebox
import os
import shutil


class OrderByExtensions:
    """Functions of creation folders and sort files by extensions given a dictionary.

    Attributes
    ---------------
    path: str
        absolute path of the directory of files to organize.
    dictionary: dict
        contains folder rules and file extensions
        - key folder name
        - values list of str(extensions)

    Methods
    ---------------
    create_directory()
        create folders named after dictionary keys at given path.

    move(folder_name=str, extension_list=list, file=str, extension=str)
        move the file only if its extension is listed.

    order()
        get the list of files the path and iterate over the dictionary and
        the file list moving the files with the move method.
    """

    def __init__(self, path, dictionary):
        self.path = path
        self.dictionary = dictionary

    def create_directory(self):
        try:
            for key, value in self.dictionary.items():
                if not os.path.isdir(self.path + '\\' + key):
                    os.mkdir(self.path + '\\' + key)
            if not os.mkdir(self.path + '\\' + 'Others'):
                os.mkdir(self.path + '\\' + 'Others')
        except FileExistsError:
            return
        except OSError as e:
            messagebox.showerror('ERROR', f'{e}')
            raise

    def move(self, folder_name, extension_list, file, extension):
        if extension in extension_list:
            shutil.move(self.path + '\\' + file, self.path + '\\' + folder_name)

    def order(self):
        file_list = os.listdir(self.path)
        extension = None
        for file in file_list:
            for key, value in self.dictionary.items():
                file_name, extension = os.path.splitext(file)
                self.move(key, value, file, extension)
            if os.path.isfile(self.path + '\\' + file):
                if extension != '':
                    shutil.move(self.path + '\\' + file, self.path + '\\' + 'Others')


class OrderByKeywords:
    """Functions of creation folders and sort files by keywords given a dictionary.

    Attributes
    ---------------
    path: str
        absolute path of the directory of files to organize.
    dictionary: dict
        contains folder rules and file keywords
        - key folder name
        - values list of str(keywords)

    Methods
    ---------------
    create_directory()
        create folders named after dictionary keys at given path.

    move(folder_name=str, keywords=list, file_name=str)
        iterates over the list keywords, check if this string is contained
        in the filename if so the move.

    order()
        get the list of files the path and iterate over the dictionary and
        the file list moving the files with the move method.
    """

    def __init__(self, path, dictionary):
        self.path = path
        self.dictionary = dictionary

    def create_directory(self):
        try:
            for key, value in self.dictionary.items():
                if not os.path.isdir(self.path + '\\' + key):
                    os.mkdir(self.path + '\\' + key)
        except FileExistsError:
            return
        except OSError as e:
            messagebox.showerror('ERROR', f'{e}')
            raise

    def move(self, folder_name, keywords, file_name):
        for keyword in keywords:
            options = [keyword.upper(), keyword.lower(), keyword.capitalize(),
                       keyword.title(), keyword.swapcase()]
            for option in options:
                if option in file_name:
                    if os.path.isfile(self.path + '\\' + file_name):
                        shutil.move(self.path + '\\' + file_name, self.path + '\\' + folder_name)

    def order(self):
        file_list = os.listdir(self.path)
        for file in file_list:
            for key, values in self.dictionary.items():
                self.move(key, values, file)
