"""Encrypt page UI for CryptoLab."""

import customtkinter as ctk
from tkinter import messagebox
from crypto_utils import encrypt_message


class EncryptPage(ctk.CTkFrame):
    """Page for encrypting plaintext messages."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._build_page()

    def _build_page(self):
        heading = ctk.CTkLabel(
            self,
            text="تشفير النص",
            font=ctk.CTkFont(size=28, weight="bold"),
            anchor="e",
        )
        heading.grid(row=0, column=0, sticky="w", pady=(10, 20))

        description = ctk.CTkLabel(
            self,
            text="اكتب الرسالة ثم اضغط تشفير. سيظهر النص المشفَّر أدناه.",
            anchor="e",
            wraplength=820,
            justify="right",
            text_color="#d0d8e7",
        )
        description.grid(row=1, column=0, sticky="w", pady=(0, 15))

        self.input_text = ctk.CTkTextbox(self, width=820, height=180)
        self.input_text.grid(row=2, column=0, pady=(0, 15), sticky="nsew")

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=3, column=0, sticky="w", pady=(0, 15))

        encrypt_button = ctk.CTkButton(
            button_frame,
            text="تشفير",
            command=self.encrypt_text,
            width=140,
            height=50,
        )
        encrypt_button.grid(row=0, column=0, padx=(0, 10))

        paste_button = ctk.CTkButton(
            button_frame,
            text="لصق من الحافظة",
            command=self.paste_input,
            width=160,
            height=50,
        )
        paste_button.grid(row=0, column=1, padx=(0, 10))

        copy_button = ctk.CTkButton(
            button_frame,
            text="نسخ النتيجة",
            command=self.copy_result,
            width=140,
            height=50,
        )
        copy_button.grid(row=0, column=2)

        self.output_text = ctk.CTkTextbox(self, width=820, height=180)
        self.output_text.grid(row=4, column=0, pady=(0, 15), sticky="nsew")

        note = ctk.CTkLabel(
            self,
            text="هل تحتاج إلى مفتاح؟ انتقل إلى قسم المفاتيح لتوليد أو تحميل مفتاح Fernet.",
            anchor="e",
            wraplength=820,
            justify="right",
            text_color="#99a3b5",
        )
        note.grid(row=5, column=0, sticky="w")

        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def encrypt_text(self):
        plaintext = self.input_text.get("1.0", "end").strip()
        try:
            if not plaintext:
                raise ValueError("يرجى إدخال نص لتشفيره.")
            if self.app.current_key is None:
                raise ValueError("حمل أو أنشئ مفتاحاً قبل التشفير.")

            encrypted = encrypt_message(self.app.current_key, plaintext)
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", encrypted)
            self.app.display_status("Text encrypted successfully.", success=True)
        except Exception as error:
            messagebox.showerror("خطأ في التشفير", str(error))
            self.app.display_status("فشل التشفير. تحقق من المفتاح والنص.", success=False)

    def paste_input(self):
        try:
            clipboard_text = self.clipboard_get().strip()
            if clipboard_text:
                self.input_text.delete("1.0", "end")
                self.input_text.insert("1.0", clipboard_text)
                self.app.display_status("تم لصق النص من الحافظة.", success=True)
            else:
                messagebox.showwarning("تنبيه اللصق", "الحافظة فارغة.")
        except Exception:
            messagebox.showwarning("خطأ اللصق", "لا يمكن الوصول إلى محتوى الحافظة.")

    def copy_result(self):
        result = self.output_text.get("1.0", "end").strip()
        if not result:
            messagebox.showwarning("تنبيه النسخ", "لا يوجد نص مشفَّر للنسخ.")
            return

        self.clipboard_clear()
        self.clipboard_append(result)
        messagebox.showinfo("تم النسخ", "تم نسخ النص المشفَّر إلى الحافظة.")
        self.app.display_status("تم نسخ النتيجة.", success=True)
