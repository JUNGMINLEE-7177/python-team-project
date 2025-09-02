import tkinter as tk
from tkinter import messagebox

def say_hello():
    name = entry.get()
    messagebox.showinfo("인사", f"안녕하세요, {name}님!")

root = tk.Tk()
root.title("Hello GUI")

tk.Label(root, text="이름을 입력하세요").pack(padx=20, pady=(20, 5))
entry = tk.Entry(root, width=20)
entry.pack(padx=20, pady=5)

tk.Button(root, text="확인", command=say_hello).pack(padx=20, pady=(5, 20))

root.mainloop()

