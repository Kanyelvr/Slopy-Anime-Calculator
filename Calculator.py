import tkinter as tk
from tkinter import messagebox
import requests
import random
import os
from PIL import Image, ImageTk
API_URL = "https://api.waifu.pics/sfw/waifu"
IMAGE_DIR = "anime_images"
os.makedirs(IMAGE_DIR, exist_ok=True)
BG = "#121212"
FG = "#e0e0e0"
BTN = "#1f1f1f"
ACCENT = "#bb86fc"
history_data = []
current_image = None
def download_anime():
    try:
        url = requests.get(API_URL).json()["url"]
        img = requests.get(url).content
        path = f"{IMAGE_DIR}/anime_{random.randint(1000,9999)}.jpg"
        with open(path, "wb") as f:
            f.write(img)
        return path
    except:
        return None
def show_image(path):
    global current_image
    if not path:
        return
    img = Image.open(path)
    current_image = img
    resize_image()
def resize_image(event=None):
    global current_image
    if current_image:
        w = center.winfo_width()
        h = center.winfo_height()
        img = current_image.copy()
        img.thumbnail((w-20, h-20))
        photo = ImageTk.PhotoImage(img)
        anime_label.config(image=photo)
        anime_label.image = photo
def evaluate_expression(event=None):
    expr = entry.get()
    if not expr.strip():
        return
    try:
        
        result = eval(expr, {"__builtins__": None}, {"abs": abs, "round": round, "pow": pow, "sqrt": lambda x: x**0.5, "sin": __import__("math").sin, "cos": __import__("math").cos, "tan": __import__("math").tan, "log": __import__("math").log10})
        full_expr = f"{expr}={result}"
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
        
        image_path = download_anime()
        show_image(image_path)
        history_data.append({"text": full_expr, "image": image_path})
        history_list.insert(tk.END, full_expr)
        history_list.yview(tk.END)
        
    except Exception as e:
        messagebox.showerror("Error", f"Invalid expression:\n{e}")
def history_select(event):
    if not history_list.curselection():
        return
    index = history_list.curselection()[0]
    item = history_data[index]
    show_image(item["image"])
    entry.delete(0, tk.END)
    entry.insert(0, item["text"].split('=')[-1])
def toggle_shortcuts():
    if shortcuts_frame.winfo_ismapped():
        shortcuts_frame.pack_forget()
    else:
        shortcuts_frame.pack(side="bottom", fill="x", padx=15, pady=5)
root = tk.Tk()
root.title("Advanced Anime Calculator")
root.geometry("900x500")
root.configure(bg=BG)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
left = tk.Frame(root, bg=BG, width=250)
left.grid(row=0, column=0, sticky="ns", padx=15, pady=15)
left.grid_propagate(False)
tk.Label(left, text="Expression", bg=BG, fg=FG, font=("Helvetica", 12, "bold")).pack(anchor="w", pady=(0,5))
entry = tk.Entry(left, bg=BTN, fg=FG, font=("Helvetica", 12))
entry.pack(fill="x", pady=(0,10))
entry.bind("<Return>", evaluate_expression)
tk.Button(left, text="CALCULATE", bg=ACCENT, fg=BG, font=("Helvetica", 12, "bold"),
          command=evaluate_expression).pack(fill="x", pady=10)

tk.Button(left, text="SHOW / HIDE SHORTCUTS", bg=BTN, fg=FG, font=("Helvetica", 10, "bold"),
          command=toggle_shortcuts).pack(fill="x", pady=5)
result_label = tk.Label(left, text="Result will appear here", bg=BG, fg=FG, font=("Helvetica", 12))
result_label.pack(pady=5)
shortcuts_frame = tk.Frame(left, bg=BTN)
shortcut_text = (
    "Shortcuts / Operators:\n"
    "+  : Addition\n"
    "-  : Subtraction\n"
    "*  : Multiplication\n"
    "/  : Division\n"
    "x^y: Power\n"
    "√x : Square root\n"
    "%  : Percent\n"
    "sin, cos, tan : Trig functions (degrees)\n"
    "log : Log base 10\n"
    "|x| : Absolute value"
)
tk.Label(shortcuts_frame, text=shortcut_text, bg=BTN, fg=FG, justify="left", font=("Helvetica", 10)).pack(padx=5, pady=5)

center = tk.Frame(root, bg=BG)
center.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
center.grid_rowconfigure(0, weight=1)
center.grid_columnconfigure(0, weight=1)
anime_label = tk.Label(center, bg=BG)
anime_label.grid(row=0, column=0, sticky="nsew")
center.bind("<Configure>", resize_image)
right = tk.Frame(root, bg=BG, width=300)
right.grid(row=0, column=2, sticky="ns", padx=15, pady=15)
right.grid_propagate(False)
tk.Label(right, text="Calculation History", bg=BG, fg=FG, font=("Helvetica", 12, "bold")).pack(anchor="w", pady=(0,5))
history_list = tk.Listbox(right, bg=BTN, fg=FG, height=25, font=("Helvetica", 11))
history_list.pack(fill="both", expand=True)
history_list.bind("<<ListboxSelect>>", history_select)
root.mainloop()
