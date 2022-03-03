import tkinter as tk
from tkinter import ttk, messagebox
from admin import read, write  # Import read and write functions from json files.
import style


class ExtensionSortWindow(tk.Toplevel):
    def __init__(self, manager):
        super().__init__()
        self.title('Configuration - Rules Folder: Extensions')
        self.resizable(False, False)
        # Main Window object to manipulate the attribute containing the extensions dictionary.
        self.__manager = manager
        self.__folder_selected = None  # Selected folder from listbox.
        self.__folder_name = None  # Text Entry -> New Folder Name.
        self.__lb_folders = None  # ListBox -> Folder list.
        self.__txt_extensions = None  # Text Entry -> Extensions that will be saved in the folder.
        self.__file_json = 'config\\extensions.json'  # Relative path of json extensions file.
        self.init_widgets()
        self.read_config()
        self.read_folder_name()

    def init_widgets(self):
        """Initialize all window's widgets."""

        top_frame = ttk.LabelFrame(self, text='New Rule Extension')
        top_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=5)
        self.__folder_name = ttk.Entry(top_frame, width=30)
        self.__folder_name.pack(side=tk.LEFT, fill=tk.X, padx=2, expand=True)
        ttk.Button(
            top_frame,
            text='New',
            command=self.load_folder_name
        ).pack(
            side=tk.LEFT,
            fill=tk.X
        )
        middle_frame = tk.Frame(self)
        middle_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5, expand=True)
        self.__lb_folders = tk.Listbox(
            middle_frame, background=style.SECONDARY_COLOR, cursor='hand2')
        self.__lb_folders.bind('<<ListboxSelect>>', self.on_select)
        self.__lb_folders.grid(row=0, column=0, rowspan=3)
        self.__txt_extensions = tk.Text(middle_frame, width=30, height=10)
        self.__txt_extensions.grid(row=0, column=1, rowspan=3)
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side=tk.TOP, fill=tk.X)
        ttk.Button(
            bottom_frame,
            text='DELETE',
            command=self.delete
        ).pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True
        )
        ttk.Button(
            bottom_frame,
            text='LOAD',
            command=self.load_extensions
        ).pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True
        )
        ttk.Button(
            self,
            text='SAVE ALL SETTINGS',
            command=self.write_config
        ).pack(
            side=tk.BOTTOM,
            fill=tk.X,
            expand=True
        )

    def on_select(self, event):
        """Show the values of the selected key into listbox widget."""

        try:
            sender = event.widget
            idx = sender.curselection()
            self.__folder_selected = sender.get(idx)
            self.read_extensions()
        except Exception:
            return

    def read_config(self):
        """Query and save the config dictionary.

        Read dictionary of json file and save it in
        the extensions_data attribute of the manager.
        """

        try:
            self.__manager.extensions_data = read(self.__file_json)
        except FileNotFoundError as e:
            messagebox.showerror('ERROR', f'Configuration file was not found: {e}')

    def read_folder_name(self):
        """Insert dictionary keys into the listbox widget.

        Checks that dictionary exists and then iterates over it
        by removing the records from the listbox widget and inserting
        the keys from the dictionary.
        """

        try:
            if self.__manager.extensions_data is not None:
                self.__lb_folders.delete(0, tk.END)
                for key, values in self.__manager.extensions_data.items():
                    self.__lb_folders.insert(tk.END, key)
        except Exception as e:
            messagebox.showerror('ERROR', f'A configuration reading error has occurred: {e}')
        finally:
            if self.__manager.extensions_data is None:
                self.read_config()

    def read_extensions(self):
        """Show dictionary values in the text widget.

        Get a value dictionary and fills a text widget text with it.
        """

        if self.__folder_selected is not None:
            key = self.__folder_selected
            chain_ext = ''
            for extension in self.__manager.extensions_data[key]:
                chain_ext += f'{extension}; '
            self.__txt_extensions.delete("1.0", "end")
            self.__txt_extensions.insert(tk.INSERT, chain_ext)

    def load_extensions(self):
        """Get the text of the text widget and update the value in the dictionary."""

        if self.__folder_selected is not None:
            ext_text = self.__txt_extensions.get(1.0, tk.END + '-1c')
            ext_text = ext_text.replace(' ', '')
            ext_list = ext_text.split(';')
            for i in range(len(ext_list)):
                if ext_list[i] == '':
                    ext_list.pop(i)
            self.__manager.extensions_data[self.__folder_selected] = ext_list
            messagebox.showinfo('LOAD', 'The configurations have been loaded successfully')
        else:
            return

    def load_folder_name(self):
        """Add a key dictionary and update the window."""

        try:
            if self.__folder_name.get() != '':
                self.__manager.extensions_data[self.__folder_name.get()] = []
                self.read_folder_name()
                self.__folder_name.delete(0, tk.END)
        except Exception:
            messagebox.showerror('ERROR', 'a configuration write error has occurred')

    def delete(self):
        """Remove key from dictionary"""

        try:
            if self.__folder_selected is not None:
                ans = messagebox.askquestion('DELETE FOLDER RULE',
                                             f'Are you sure you want to delete the {self.__folder_selected} folder rule?')
                if ans == 'yes':
                    del self.__manager.extensions_data[self.__folder_selected]
                    self.__txt_extensions.delete("1.0", "end")
                    self.read_folder_name()
                    self.__folder_selected = None
        except KeyError as e:
            messagebox.showerror('ERROR', f'The rule you want to delete does not exist: {e}')

    def write_config(self):
        """Write the changes to the config file (json)."""

        try:
            write(self.__manager.extensions_data, self.__file_json)
            messagebox.showinfo('SAVE ALL SETTINGS',
                                'The configuration has been saved successfully.')
        except Exception as e:
            messagebox.showerror('ERROR', f'An unexpected error has occurred: {e}')
