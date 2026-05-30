"""Hash generator page UI for CryptoLab."""

import customtkinter as ctk
from tkinter import messagebox
from hash_utils import generate_hash


class HashPage(ctk.CTkFrame):
    """Page for generating MD5 and SHA-256 hashes."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._build_page()

    def _build_page(self):
        heading = ctk.CTkLabel(
            self,
            text="مولد الهاش",
            font=ctk.CTkFont(size=28, weight="bold"),
            anchor="e",
        )
        heading.grid(row=0, column=0, sticky="w", pady=(10, 20))

        description = ctk.CTkLabel(
            self,
            text="أنشئ هاش باستخدام MD5 أو SHA-256. الهاش اتجاه واحد ومفيد للتأكد من سلامة البيانات.",
            anchor="e",
            wraplength=760,
            justify="right",
        )
        description.grid(row=1, column=0, sticky="w", pady=(0, 15))

        self.algorithm_menu = ctk.CTkOptionMenu(
            self,
            values=["MD5", "SHA-256"],
            command=self._update_algorithm_label,
            width=180,
        )
        self.algorithm_menu.set("SHA-256")
        self.algorithm_menu.grid(row=2, column=0, sticky="w", pady=(0, 10))

        self.input_text = ctk.CTkTextbox(self, width=820, height=180)
        self.input_text.grid(row=3, column=0, pady=(0, 15), sticky="nsew")

        hash_button = ctk.CTkButton(
            self,
            text="توليد هاش",
            command=self.generate_hash_value,
            width=180,
        )
        hash_button.grid(row=4, column=0, pady=(0, 15), sticky="w")

        self.output_text = ctk.CTkTextbox(self, width=820, height=180)
        self.output_text.grid(row=5, column=0, pady=(0, 15), sticky="nsew")
        self.output_text.configure(state="normal")

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=6, column=0, sticky="w", pady=(0, 10))

        copy_button = ctk.CTkButton(
            button_frame,
            text="نسخ الهاش",
            command=self.copy_hash,
            width=180,
            height=50,
        )
        copy_button.grid(row=0, column=0)

        self.algorithm_label = ctk.CTkLabel(
            self,
            text="الخوارزمية المختارة: SHA-256",
            anchor="e",
            text_color="#99a3b5",
        )
        self.algorithm_label.grid(row=6, column=0, sticky="w")

        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _update_algorithm_label(self, selected_algorithm):
        self.algorithm_label.configure(text=f"الخوارزمية المختارة: {selected_algorithm}")

    def generate_hash_value(self):
        text = self.input_text.get("1.0", "end").strip()
        algorithm = self.algorithm_menu.get()
        try:
            digest = generate_hash(algorithm, text)
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", digest)
            self.app.display_status(f"تم توليد هاش {algorithm}.", success=True)
        except Exception as error:
            messagebox.showerror("خطأ في الهاش", str(error))
            self.app.display_status("فشل توليد الهاش. تحقق من المدخلات.", success=False)

    def copy_hash(self):
        result = self.output_text.get("1.0", "end").strip()
        if not result:
            messagebox.showwarning("تنبيه النسخ", "لا يوجد هاش للنسخ.")
            return

        self.clipboard_clear()
        self.clipboard_append(result)
        messagebox.showinfo("تم النسخ", "تم نسخ الهاش إلى الحافظة.")
        self.app.display_status("تم نسخ الهاش.", success=True)
