import customtkinter as ctk
from gui.app import App


def main():
    ctk.set_appearance_mode("System")  # "Dark", "Light", or "System"
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()