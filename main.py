import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import string
import pyperclip

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

def caesar_cipher(text, shift, encrypt=True):
    result = ""
    shift = shift if encrypt else -shift
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

def affine_cipher(text, a, b, encrypt=True):
    def affine_char(c, a, b, encrypt):
        if c.isalpha():
            base = 65 if c.isupper() else 97
            c = ord(c) - base
            if encrypt:
                result = (a * c + b) % 26
            else:
                a_inv = mod_inverse(a, 26)
                result = (a_inv * (c - b)) % 26
            return chr(result + base)
        else:
            return c

    return ''.join(affine_char(c, a, b, encrypt) for c in text)

def substitution_cipher(text, key, encrypt=True):
    alphabet_upper = string.ascii_uppercase
    alphabet_lower = string.ascii_lowercase
    key_upper = key.upper()
    key_lower = key.lower()

    if not is_valid_key(key_upper):
        raise ValueError

    if encrypt:
        table_upper = str.maketrans(alphabet_upper, key_upper)
        table_lower = str.maketrans(alphabet_lower, key_lower)
    else:
        table_upper = str.maketrans(key_upper, alphabet_upper)
        table_lower = str.maketrans(key_lower, alphabet_lower)

    encrypted_text = text.translate(table_upper)
    encrypted_text = encrypted_text.translate(table_lower)

    return encrypted_text

def is_valid_key(key):
    return len(key) == 26 and len(set(key)) == 26

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, file.read())

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(result_text.get("1.0", tk.END))

def copy_result():
    result = result_text.get("1.0", tk.END)
    pyperclip.copy(result.strip())

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError
    else:
        return x % m

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def process_text():
    algorithm = algorithm_var.get()
    input_str = input_text.get("1.0", tk.END).strip()
    shift = int(shift_entry.get()) if shift_entry.get().isdigit() else 0
    a = int(a_entry.get()) if a_entry.get().isdigit() else 1
    b = int(b_entry.get()) if b_entry.get().isdigit() else 0
    key = substitution_entry.get()
    mode = mode_var.get()

    if algorithm == "Caesar":
        result = caesar_cipher(input_str, shift, encrypt = (mode == "Mã hóa"))
    elif algorithm == "Affine":
        result = affine_cipher(input_str, a, b, encrypt = (mode == "Mã hóa"))
    elif algorithm == "Substitution":
        result = substitution_cipher(input_str, key, encrypt = (mode == "Mã hóa"))

    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, result)

app = ctk.CTk()
app.title("Mã hóa & Giải mã văn bản")
app.geometry("900x750")

title_label = ctk.CTkLabel(app, text = "Chương trình Mã hóa & Giải mã văn bản", font=("Arial", 20))
title_label.pack(pady = 10)

input_frame = ctk.CTkFrame(app)
input_frame.pack(pady = 10, padx = 10, fill = "x")

input_label = ctk.CTkLabel(input_frame, text = "Nhập đoạn văn bản:")
input_label.pack(anchor = "w", padx = 10, pady = 5)

input_text = ctk.CTkTextbox(input_frame, height = 100)
input_text.pack(padx = 10, pady = 5, fill = "x")

algorithm_var = ctk.StringVar(value = "Caesar")
algorithm_label = ctk.CTkLabel(app, text = "Chọn thuật toán:")
algorithm_label.pack(anchor = "w", padx = 10)

algorithm_options = ctk.CTkOptionMenu(app, values = ["Caesar", "Affine", "Substitution"], variable = algorithm_var)
algorithm_options.pack(pady = 5)

mode_var = ctk.StringVar(value = "Mã hóa")
mode_label = ctk.CTkLabel(app, text = "Chọn chế độ:")
mode_label.pack(anchor = "w", padx = 10)

mode_options = ctk.CTkOptionMenu(app, values = ["Mã hóa", "Giải mã"], variable = mode_var)
mode_options.pack(pady = 5)

param_frame = ctk.CTkFrame(app)
param_frame.pack(pady = 10)

shift_label = ctk.CTkLabel(param_frame, text = "Shift (cho Caesar):")
shift_label.grid(row = 0, column = 0, padx = 10)

shift_entry = ctk.CTkEntry(param_frame)
shift_entry.grid(row = 0, column = 1, padx = 10)

a_label = ctk.CTkLabel(param_frame, text = "Khóa a (cho Affine):")
a_label.grid(row = 1, column = 0, padx = 10)

a_entry = ctk.CTkEntry(param_frame)
a_entry.grid(row = 1, column = 1, padx = 10)

b_label = ctk.CTkLabel(param_frame, text = "Khóa b (cho Affine):")
b_label.grid(row = 2, column = 0, padx = 10)

b_entry = ctk.CTkEntry(param_frame)
b_entry.grid(row = 2, column = 1, padx = 10)

substitution_label = ctk.CTkLabel(param_frame, text = "Key (cho Substitution):")
substitution_label.grid(row = 3, column = 0, padx = 10)

substitution_entry = ctk.CTkEntry(param_frame)
substitution_entry.grid(row = 3, column = 1, padx = 10)

process_button = ctk.CTkButton(app, text = "Thực hiện", command = process_text)
process_button.pack(pady = 10)

result_frame = ctk.CTkFrame(app)
result_frame.pack(pady = 10, padx = 10, fill = "x")

result_label = ctk.CTkLabel(result_frame, text = "Kết quả:")
result_label.pack(anchor = "w", padx = 10, pady = 5)

result_text = ctk.CTkTextbox(result_frame, height = 100)
result_text.pack(padx = 10, pady = 5, fill = "x")

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady = 10)

open_button = ctk.CTkButton(button_frame, text = "Mở File", command = open_file)
open_button.grid(row = 0, column = 0, padx = 10)

save_button = ctk.CTkButton(button_frame, text = "Lưu File", command = save_file)
save_button.grid(row = 0, column = 1, padx = 10)

copy_button = ctk.CTkButton(button_frame, text = "Sao chép kết quả", command = copy_result)
copy_button.grid(row = 0, column = 2, padx = 10)

app.mainloop()

"""
by 23010680 | Nguyen Quoc Thien | Cantho City | K17 - Computer Science_1 - Phenikaa University
"""