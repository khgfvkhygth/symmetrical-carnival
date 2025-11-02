import tkinter as tk

# Create a window with transparent rectangle for OCR alignment
root = tk.Tk()
root.title("📸 OCR Target Area")
root.geometry("180x70+100+200")
root.configure(bg='black')
root.attributes("-topmost", True)
root.attributes("-alpha", 0.3)

label = tk.Label(root, text="🟥 Place this over the
Bustabit Multiplier", font=("Arial", 9), bg="black", fg="white")
label.pack(expand=True)

root.mainloop()