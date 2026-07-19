import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageTk
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
import os

class QRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom QR Code Generator")
        self.root.geometry("700x650")
        self.root.configure(bg="#E9F1FA")

        # --- Variables ---
        self.data = tk.StringVar()
        self.box_size = tk.IntVar(value=10)
        self.border = tk.IntVar(value=4)
        self.fill_color = "#000000"
        self.back_color = "#FFFFFF"
        self.error_correction = tk.StringVar(value="M")
        self.qr_image = None
        self.logo_path = None

        # --- Layout ---
        tk.Label(root, text="Enter URL or Text:", bg="#E9F1FA", font=("Arial", 12)).pack(pady=5)
        tk.Entry(root, textvariable=self.data, width=60, font=("Arial", 11)).pack(pady=5)

        tk.Label(root, text="Error Correction Level:", bg="#E9F1FA").pack()
        tk.OptionMenu(root, self.error_correction, "L", "M", "Q", "H").pack(pady=5)

        frame = tk.Frame(root, bg="#E9F1FA")
        frame.pack(pady=10)
        tk.Label(frame, text="Box Size:", bg="#E9F1FA").grid(row=0, column=0)
        tk.Spinbox(frame, from_=1, to=20, textvariable=self.box_size, width=5).grid(row=0, column=1, padx=5)
        tk.Label(frame, text="Border:", bg="#E9F1FA").grid(row=0, column=2)
        tk.Spinbox(frame, from_=1, to=10, textvariable=self.border, width=5).grid(row=0, column=3, padx=5)

        color_frame = tk.Frame(root, bg="#E9F1FA")
        color_frame.pack(pady=5)
        tk.Button(color_frame, text="Choose Fill Color", command=self.choose_fill_color, bg="#C8E4F9").grid(row=0, column=0, padx=10)
        tk.Button(color_frame, text="Choose Background Color", command=self.choose_back_color, bg="#C8E4F9").grid(row=0, column=1, padx=10)

        logo_frame = tk.Frame(root, bg="#E9F1FA")
        logo_frame.pack(pady=5)
        tk.Button(logo_frame, text="Add Logo", command=self.add_logo, bg="#A5D6A7").grid(row=0, column=0, padx=10)

        tk.Button(root, text="Generate QR Code", command=self.generate_qr, bg="#FFD700", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Button(root, text="Save QR Code", command=self.save_qr, bg="#90CAF9").pack(pady=5)
        tk.Button(root, text="Reset / Clear", command=self.reset_all, bg="#FFB6C1").pack(pady=5)

        # Canvas for preview
        self.canvas = tk.Label(root, bg="#FFFFFF", relief="solid", width=250, height=250)
        self.canvas.pack(pady=15, ipadx=10, ipady=10)

    # ---------- Functions ----------

    def choose_fill_color(self):
        color = colorchooser.askcolor(title="Choose Fill Color")
        if color[1]:
            self.fill_color = color[1]

    def choose_back_color(self):
        color = colorchooser.askcolor(title="Choose Background Color")
        if color[1]:
            self.back_color = color[1]

    def add_logo(self):
        path = filedialog.askopenfilename(
            title="Select Logo Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if path:
            self.logo_path = path
            messagebox.showinfo("Logo Added", f"Logo loaded: {os.path.basename(path)}")

    def generate_qr(self):
        data = self.data.get().strip()
        if not data:
            messagebox.showwarning("Input Required", "Please enter text or URL.")
            return

        ec_map = {
            "L": ERROR_CORRECT_L,
            "M": ERROR_CORRECT_M,
            "Q": ERROR_CORRECT_Q,
            "H": ERROR_CORRECT_H
        }

        qr = qrcode.QRCode(
            version=None,
            error_correction=ec_map[self.error_correction.get()],
            box_size=self.box_size.get(),
            border=self.border.get(),
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color=self.fill_color, back_color=self.back_color).convert("RGBA")

        # Add logo if selected
        if self.logo_path:
            try:
                logo = Image.open(self.logo_path).convert("RGBA")
                qr_w, qr_h = img.size
                logo_w = qr_w // 5
                logo = logo.resize((logo_w, logo_w))
                pos = ((qr_w - logo_w) // 2, (qr_h - logo_w) // 2)
                img.paste(logo, pos, logo)
            except Exception as e:
                messagebox.showerror("Logo Error", str(e))

        self.qr_image = img

        # Preview in Tkinter
        img_preview = img.resize((250, 250))
        self.tk_image = ImageTk.PhotoImage(img_preview)
        self.canvas.config(image=self.tk_image)
        self.canvas.image = self.tk_image

    def save_qr(self):
        if not self.qr_image:
            messagebox.showwarning("No QR Code", "Please generate a QR code first!")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All Files", "*.*")]
        )
        if file_path:
            self.qr_image.save(file_path)
            messagebox.showinfo("Saved", f"QR code saved as {file_path}")

    def reset_all(self):
        """Reset all settings and clear the preview"""
        self.data.set("")
        self.box_size.set(10)
        self.border.set(4)
        self.fill_color = "#000000"
        self.back_color = "#FFFFFF"
        self.error_correction.set("M")
        self.logo_path = None
        self.qr_image = None

        # Clear preview
        self.canvas.config(image="", bg="#FFFFFF")
        messagebox.showinfo("Reset", "All fields have been cleared!")

# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = QRApp(root)
    root.mainloop()
