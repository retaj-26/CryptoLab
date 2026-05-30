"""Key management page UI for CryptoLab."""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from crypto_utils import generate_key
from key_manager import load_key, save_key


class KeysPage(ctk.CTkFrame):
    """Page for generating, saving, and loading encryption keys."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._build_page()

    def _build_page(self):
        heading = ctk.CTkLabel(
            self,
            text="إدارة المفاتيح",
            font=ctk.CTkFont(size=28, weight="bold"),
            anchor="e",
        )
        heading.grid(row=0, column=0, sticky="w", pady=(10, 20))

        description = ctk.CTkLabel(
            self,
            text="مفتاح Fernet مطلوب للتشفير وفك التشفير. يمكنك توليد مفتاح، حفظه، أو تحميل مفتاح محفوظ.",
            anchor="e",
            wraplength=760,
            justify="right",
        )
        description.grid(row=1, column=0, sticky="w", pady=(0, 15))

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=0, sticky="w", pady=(0, 10))

        generate_button = ctk.CTkButton(button_frame, text="توليد مفتاح", command=self.generate_new_key)
        generate_button.grid(row=0, column=0, padx=(0, 10))

        save_button = ctk.CTkButton(button_frame, text="حفظ المفتاح", command=self.save_current_key)
        save_button.grid(row=0, column=1, padx=(0, 10))

        load_button = ctk.CTkButton(button_frame, text="تحميل مفتاح", command=self.load_key_file)
        load_button.grid(row=0, column=2, padx=(0, 10))

        copy_key_button = ctk.CTkButton(button_frame, text="نسخ المفتاح", command=self.copy_key)
        copy_key_button.grid(row=0, column=3)

        self.key_display = ctk.CTkTextbox(self, width=820, height=120)
        self.key_display.grid(row=3, column=0, pady=(0, 15), sticky="nsew")
        self.key_display.configure(state="disabled")

        note = ctk.CTkLabel(
            self,
            text="حافظ على مفتاحك آمناً. أي شخص يملك المفتاح يمكنه فك التشفير.",
            anchor="e",
            wraplength=760,
            justify="right",
            text_color="#99a3b5",
        )
        note.grid(row=4, column=0, sticky="w")

        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._refresh_key_display()

    def generate_new_key(self):
        self.app.current_key = generate_key()
        self._refresh_key_display()
        messagebox.showinfo("تم توليد المفتاح", "تم توليد مفتاح Fernet جديد.")
        self.app.display_status("تم توليد مفتاح جديد بنجاح.", success=True)

    def save_current_key(self):
        if self.app.current_key is None:
            messagebox.showerror("خطأ في الحفظ", "لا يوجد مفتاح محمَّل. قم بتوليد أو تحميل مفتاح أولاً.")
            self.app.display_status("فشل الحفظ. لا يوجد مفتاح.", success=False)
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Fernet Key",
            defaultextension=".key",
            filetypes=[("Key files", "*.key"), ("All files", "*")],
        )
        if not file_path:
            return

        try:
            save_key(file_path, self.app.current_key)
            messagebox.showinfo("تم الحفظ", "تم حفظ المفتاح بنجاح.")
            self.app.display_status("تم حفظ المفتاح في الملف.", success=True)
        except Exception as error:
            messagebox.showerror("خطأ في الحفظ", str(error))
            self.app.display_status("فشل حفظ المفتاح.", success=False)

    def load_key_file(self):
        file_path = filedialog.askopenfilename(
            title="Load Fernet Key",
            filetypes=[("Key files", "*.key"), ("All files", "*")],
        )
        if not file_path:
            return

        try:
            loaded_key = load_key(file_path)
            self.app.current_key = loaded_key
            self._refresh_key_display()
            messagebox.showinfo("تم التحميل", "تم تحميل المفتاح بنجاح.")
            self.app.display_status("تم تحميل المفتاح من الملف.", success=True)
        except Exception as error:
            messagebox.showerror("خطأ في التحميل", str(error))
            self.app.display_status("فشل تحميل المفتاح.", success=False)

    def _refresh_key_display(self):
        key_text = "No key loaded."
        if self.app.current_key is not None:
            key_text = self.app.current_key.decode("utf-8")

        self.key_display.configure(state="normal")
        self.key_display.delete("1.0", "end")
        self.key_display.insert("1.0", key_text)
        self.key_display.configure(state="disabled")

    def copy_key(self):
        key_text = self.key_display.get("1.0", "end").strip()
        if not key_text:
            messagebox.showwarning("تنبيه النسخ", "لا يوجد مفتاح للنسخ.")
            return

        self.clipboard_clear()
        self.clipboard_append(key_text)
        messagebox.showinfo("تم النسخ", "تم نسخ المفتاح إلى الحافظة.")
        self.app.display_status("تم نسخ المفتاح.", success=True)
