import database
from gui import FindItApp


def main():
    database.init_db()
    app = FindItApp()
    app.mainloop()


if __name__ == "__main__":
    main()
