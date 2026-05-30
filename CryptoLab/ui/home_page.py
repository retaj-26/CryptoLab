"""Home page UI for CryptoLab."""

import customtkinter as ctk


class HomePage(ctk.CTkFrame):
    """Welcome page with simple navigation for CryptoLab."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._build_page()

    def _build_page(self):
        title = ctk.CTkLabel(
            self,
            text="كريبتو لاب",
            font=ctk.CTkFont(size=36, weight="bold"),
            anchor="e",
            justify="right",
        )
        title.grid(row=0, column=0, sticky="e", pady=(20, 10), padx=(0, 20))

        subtitle = ctk.CTkLabel(
            self,
            text="تطبيق بسيط لتعلم التشفير والأمن السيبراني بطريقة مرئية وسهلة الاستخدام.",
            font=ctk.CTkFont(size=16),
            wraplength=820,
            justify="right",
            text_color="#d0d7e5",
        )
        subtitle.grid(row=1, column=0, sticky="e", pady=(0, 20), padx=(0, 20))

        quick_start = ctk.CTkFrame(self, fg_color="#15213b", corner_radius=24)
        quick_start.grid(row=2, column=0, sticky="nsew", pady=(0, 20), padx=(0, 20))
        quick_start.grid_columnconfigure((0, 1), weight=1, uniform="buttons")

        quick_start_title = ctk.CTkLabel(
            quick_start,
            text="ابدأ الآن",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="e",
            justify="right",
        )
        quick_start_title.grid(row=0, column=0, columnspan=2, sticky="e", padx=24, pady=(24, 12))

        buttons = [
            ("المفاتيح", "المفاتيح"),
            ("تشفير النص", "تشفير"),
            ("فك تشفير النص", "فك التشفير"),
            ("توليد هاش", "هاش"),
            ("شروحات تعليمية", "تعلم"),
        ]

        for index, (label, page_name) in enumerate(buttons):
            button = ctk.CTkButton(
                quick_start,
                text=label,
                command=lambda name=page_name: self.app._show_page(name),
                width=260,
                height=60,
                corner_radius=20,
            )
            button.grid(row=1 + index // 2, column=index % 2, padx=20, pady=10, sticky="ew")

        tip = ctk.CTkLabel(
            self,
            text="ابدأ دائماً بتوليد أو تحميل مفتاح من صفحة المفاتيح، ثم انتقل إلى التشفير وفك التشفير.",
            wraplength=820,
            justify="right",
            text_color="#a2adc8",
        )
        tip.grid(row=3, column=0, sticky="e", pady=(0, 10), padx=(0, 20))

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
