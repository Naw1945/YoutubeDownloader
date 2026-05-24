import os
import customtkinter as ctk
from ui.app import YoutubeDownloaderApp


def main():
    os.makedirs("downloads", exist_ok=True)
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = YoutubeDownloaderApp()
    app.mainloop()


if __name__ == "__main__":
    main()