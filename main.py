import tkinter as tk
from tkinter import ttk
import keyboard
import os
import sys
import threading
from PIL import Image, ImageDraw
import pystray


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class SkullApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Settings")
        self.root.geometry("300x200")
        self.root.protocol('WM_DELETE_WINDOW', self.hide_window)

        self.hotkey_show = "F9"
        self.hotkey_close = "F10"
        self.is_running = False

        self.create_widgets()
        self.setup_hotkeys()
        self.create_tray()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="Show Skull Hotkey:").pack()
        self.show_ent = ttk.Entry(frame)
        self.show_ent.insert(0, self.hotkey_show)
        self.show_ent.pack(pady=5)

        ttk.Label(frame, text="Exit App Hotkey:").pack()
        self.close_ent = ttk.Entry(frame)
        self.close_ent.insert(0, self.hotkey_close)
        self.close_ent.pack(pady=5)

        ttk.Button(frame, text="Save & Apply", command=self.update_hotkeys).pack(pady=10)

    def setup_hotkeys(self):
        keyboard.unhook_all()
        keyboard.add_hotkey(self.hotkey_show, lambda: self.root.after(0, self.show_skull))
        keyboard.add_hotkey(self.hotkey_close, self.close_app)

    def update_hotkeys(self):
        self.hotkey_show = self.show_ent.get()
        self.hotkey_close = self.close_ent.get()
        self.setup_hotkeys()

    def show_skull(self):
        if self.is_running:
            return
        self.is_running = True

        skull_win = tk.Toplevel(self.root)
        skull_win.overrideredirect(True)
        skull_win.attributes('-topmost', True)

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        skull_win.geometry(f"{sw}x{sh}+0+0")

        trans_color = '#000001'
        skull_win.config(bg=trans_color)
        skull_win.attributes('-transparentcolor', trans_color)
        skull_win.attributes('-alpha', 0.0)

        try:
            img_path = resource_path("skull.png")
            img = tk.PhotoImage(file=img_path)
            label = tk.Label(skull_win, image=img, bg=trans_color, bd=0, highlightthickness=0)
            label.image = img
            label.place(relx=0.5, rely=0.5, anchor="center")
        except:
            skull_win.destroy()
            self.is_running = False
            return

        def fade_in(alpha=0.0):
            if alpha < 1.0:
                alpha += 0.05
                skull_win.attributes('-alpha', min(alpha, 1.0))
                self.root.after(8, lambda: fade_in(alpha))
            else:
                self.root.after(500, fade_out)

        def fade_out(alpha=1.0):
            if alpha > 0:
                alpha -= 0.05
                skull_win.attributes('-alpha', max(alpha, 0))
                self.root.after(15, lambda: fade_out(alpha))
            else:
                skull_win.destroy()
                self.is_running = False

        fade_in()

    def hide_window(self):
        self.root.withdraw()

    def show_window(self):
        self.root.after(0, self.root.deiconify)

    def close_app(self):
        self.tray.stop()
        self.root.quit()
        os._exit(0)

    def create_tray(self):
        icon_img = Image.new('RGB', (64, 64), color=(0, 0, 0))
        d = ImageDraw.Draw(icon_img)
        d.rectangle([16, 16, 48, 48], fill=(255, 255, 255))

        menu = (
            pystray.MenuItem('Settings', self.show_window),
            pystray.MenuItem('Exit', self.close_app)
        )
        self.tray = pystray.Icon("SkullApp", icon_img, "Skull Overlay", menu)
        threading.Thread(target=self.tray.run, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = SkullApp(root)
    root.mainloop()