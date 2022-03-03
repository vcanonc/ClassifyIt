from app import App


if __name__ == '__main__':
    app = App()
    app.minsize(height=260, width=275)
    app.maxsize(height=260, width=275)
    app.iconbitmap('images/logo.ico')
    app.mainloop()
