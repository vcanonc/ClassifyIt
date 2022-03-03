import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import webbrowser  # Import module to open web pages.
from KeywordSortWindow import KeywordSortWindow  # Import keywords settings modal window.
from ExtensionSortWindow import ExtensionSortWindow  # Import extensions settings modal window.
from organizer import OrderByKeywords, OrderByExtensions  # Import file sort script.
from admin import restore_config  # Import restore function from admin script.
import style


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('ClassifyIt')
        self.resizable(False, False)
        self.__path = None
        self.__organizer = None
        self.keywords_data = None  # Keywords dictionary data for sorting files by.
        self.extensions_data = None  # Extensions dictionary data for classification of files
        # by keywords contained in the name.
        self.__mode = tk.StringVar(self, value='Keyword')
        self.__win = None  # Modal window for configure data.
        self.__lbl_path = None  # Label widget for show path chosen by user.
        self.__frame_config = None  # A frame containing configuration options.
        self.__options_frame = None
        self.__logo = None
        self.__icon = tk.PhotoImage(file='images\\logo_mini.png')
        self.init_widgets()

    def init_widgets(self):
        """Initialize all window's widgets."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Reset Data', command=self.restore_data)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.quit)
        menubar.add_cascade(label='File', menu=file_menu)
        info_menu = tk.Menu(menubar, tearoff=0)
        info_menu.add_command(label='Documentation',
                              command=lambda: os.startfile('docs/'))
        info_menu.add_command(label='About', command=self.message_about)
        menubar.add_cascade(label='Help', menu=info_menu)
        tk.Label(
            self,
            text='🗂 ClassifyIt 📎',
            justify=tk.CENTER,
            **style.STYLE_TITLE
        ).pack(
            side=tk.TOP,
            fill=tk.X
        )
        # Button and label path Frame
        frame_path = ttk.LabelFrame(self, text='Folder Path')
        frame_path.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=5)
        self.__lbl_path = ttk.Label(frame_path, text='./', relief='groove', borderwidth=2, anchor='center',
                                    background=style.SECONDARY_COLOR)
        self.__lbl_path.pack(side=tk.TOP, fill=tk.BOTH)
        ttk.Button(
            frame_path,
            text='Modify',
            command=self.browse_directory
        ).pack(
            side=tk.TOP,
            fill=tk.BOTH
        )
        # Configuration Frame
        self.__frame_config = ttk.LabelFrame(self, text='Configuration')
        self.__frame_config.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=5)
        self.__options_frame = ttk.Frame(self.__frame_config)
        self.__options_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=5, expand=True)
        ttk.Label(self.__options_frame, text='Organize by: ',
                  anchor='center').pack(side=tk.TOP, fill=tk.X)
        for i in ('Keyword', 'Extension'):
            ttk.Radiobutton(
                self.__options_frame,
                cursor='hand2',
                text=i,
                variable=self.__mode,
                value=i,
            ).pack(
                side=tk.LEFT,
                fill=tk.X,
                expand=True,
                padx=5,
                pady=5
            )
        ttk.Button(
            self.__frame_config,
            text='Configure',
            command=self.configure_mode
        ).pack(
            side=tk.TOP,
            fill=tk.BOTH
        )
        ttk.Button(
            self,
            text='START SORT',
            command=self.sort_files
        ).pack(
            side=tk.BOTTOM,
            fill=tk.X,
            padx=10,
            pady=5
        )

    def browse_directory(self):
        """Get a directory.

        generates a window for the user to select a directory,
        changes the working directory and displays it in self.__lbl_path.
        """

        directory = filedialog.askdirectory()
        if directory != "":
            os.chdir(directory)
        self.__path = os.getcwd()
        if len(os.getcwd()) <= 41:
            self.__lbl_path['text'] = self.__path
        else:
            folders = self.__path.split('\\')
            text = folders.pop()
            self.__lbl_path['text'] = f'{self.__path[:41 - len(text)]}...\\{text}'

    def configure_mode(self):
        """Initialize configuration modal window."""

        if self.__win is not None:
            self.__win.destroy()
        if self.__mode.get() == 'Keyword':
            self.__win = KeywordSortWindow(self)
        elif self.__mode.get() == 'Extension':
            self.__win = ExtensionSortWindow(self)
        self.__win.wm_iconphoto(False, self.__icon)
        self.__win.grab_set()
        self.__win.focus_set()

    def restore_data(self):
        """Reset all program settings."""
        ans = messagebox.askquestion('Warning', 'Are you sure to restore the application?\nThis will erase all your '
                                                'custom settings.')
        self.__lbl_path['text'] = './'
        self.__path = None
        if ans == 'yes':
            restore_config()
            messagebox.showinfo('RESTORE', 'Settings have been restored.')

    def sort_files(self):
        """Sort all files in the selected directory.

        Verifies that there is extensions data and keywords data
        and sorts all files contained in the selected directory.
        """

        if self.__path is not None:
            if self.keywords_data is None or self.extensions_data is None:
                messagebox.showinfo('SORT', 'Please make sure to configure all sections.')
            else:
                self.disable_frame_config()
                if self.__mode.get() == 'Keyword':
                    self.__organizer = OrderByKeywords(self.__path, self.keywords_data)
                    self.__organizer.create_directory()
                    self.__organizer.order()
                elif self.__mode.get() == 'Extension':
                    self.__organizer = OrderByExtensions(self.__path, self.extensions_data)
                    self.__organizer.create_directory()
                    self.__organizer.order()
                messagebox.showinfo('SORT', 'The files have been successfully moved')
        else:
            messagebox.showinfo('SORT', 'Please insert a directory.')

    def disable_frame_config(self):
        """Disable widgets from frame_config."""
        for child in self.__frame_config.winfo_children():
            child.state(['disabled'])
        '''for child in self.options_frame.winfo_children():
            child.state(['disabled'])'''

    def open_web_page(self, url):
        """Open a given web page in the browser."""

        webbrowser.open_new(url)

    def message_about(self):
        """Generate an information modal window."""

        make_modal = len(sys.argv) > 1
        win = tk.Toplevel()
        win.geometry("280x260")
        win.resizable(False, False)
        win.wm_iconphoto(False, self.__icon)
        self.__logo = tk.PhotoImage(file='images/logo_mini.png')
        ttk.Label(win, image=self.__logo, anchor='center').pack(padx=10, side=tk.TOP, fill=tk.BOTH)
        ttk.Label(
            win,
            text='ClassifyIt v.1.0. \nDeveloped by: Víctor Camilo Cañón \nGithub:',
            anchor='center'
        ).pack(
            padx=10,
            pady=5,
            side=tk.TOP,
            fill=tk.BOTH
        )
        link = ttk.Label(win, text='https://github.com/vcanonc',
                         foreground='blue', cursor="hand2", anchor='center')
        link.pack(padx=10, side=tk.TOP, fill=tk.BOTH)
        link.bind('<Button-1>', lambda e: self.open_web_page('https://github.com/vcanonc'))
        ttk.Button(win, text='Close', command=win.destroy).pack(
            side=tk.BOTTOM, fill=tk.X, padx=11, pady=11)
        if make_modal:
            win.focus_set()
            win.grab_set()
            win.wait_window()
