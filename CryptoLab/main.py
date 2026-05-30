"""CryptoLab main application entry point.

This module creates the CustomTkinter application window, loads the UI pages,
and manages the shared app state such as the active encryption key.
"""

import customtkinter as ctk
import webbrowser
from ui.home_page import HomePage
from ui.encrypt_page import EncryptPage
from ui.decrypt_page import DecryptPage
from ui.hash_page import HashPage
from ui.keys_page import KeysPage
from ui.learn_page import LearnPage


class CryptoLabApp(ctk.CTk):
    """Main application window for CryptoLab."""

    def __init__(self):
        super().__init__()
        self.title("كريبتو لاب - أساسيات التشفير")
        self.geometry("1080x720")
        self.minsize(960, 620)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.current_key = None
        self.active_page = None

        self._create_layout()
        self._create_sidebar()
        self._create_status_bar()
        self._show_page("الرئيسية")

    def _create_layout(self):
        """Create the main layout for the sidebar and content area."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color="#101924")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)

        self.content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 10), pady=(10, 10))
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

    def _create_sidebar(self):
        """Build the navigation sidebar with simple buttons."""
        app_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="كريبتو لاب",
            font=ctk.CTkFont(size=26, weight="bold"),
            pady=16,
            justify="right",
        )
        app_label.grid(row=0, column=0, padx=18, pady=(20, 10), sticky="e")

        pages = ["الرئيسية", "المفاتيح", "تشفير", "فك التشفير", "هاش", "تعلم"]
        for index, page_name in enumerate(pages, start=1):
            button = ctk.CTkButton(
                self.sidebar_frame,
                text=page_name,
                command=lambda name=page_name: self._show_page(name),
                width=210,
                height=52,
                corner_radius=16,
                hover_color="#1f3b63",
            )
            button.grid(row=index, column=0, padx=15, pady=7)

        footer = ctk.CTkLabel(
            self.sidebar_frame,
            text="صُمم هذا التطبيق لتعلم الأمن السيبراني بسهولة.",
            font=ctk.CTkFont(size=11),
            wraplength=210,
            justify="right",
            fg_color="transparent",
            text_color="#9aa5b9",
        )
        footer.grid(row=7, column=0, padx=15, pady=(24, 4), sticky="s")

        linkedin_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="in : Retaj Alharbi",
            font=ctk.CTkFont(size=12, weight="bold"),
            wraplength=210,
            justify="right",
            fg_color="transparent",
            text_color="#70a9ff",
            cursor="hand2",
        )
        linkedin_label.grid(row=8, column=0, padx=15, pady=(0, 20), sticky="s")
        linkedin_label.bind(
            "<Button-1>",
            lambda event: webbrowser.open(
                "https://www.linkedin.com/in/retaj-alharbi-153057319/?skipRedirect=true"
            ),
        )

    def _create_status_bar(self):
        """Add a small status label at the bottom of the app."""
        self.status_label = ctk.CTkLabel(
            self,
            text="جاهز",
            anchor="e",
            fg_color="#11161f",
            text_color="#aab3c9",
            height=34,
            justify="right",
        )
        self.status_label.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

    def _show_page(self, page_name: str):
        """Display the selected page inside the content area."""
        if self.active_page is not None:
            self.active_page.grid_forget()

        page_classes = {
            "الرئيسية": HomePage,
            "تشفير": EncryptPage,
            "فك التشفير": DecryptPage,
            "هاش": HashPage,
            "المفاتيح": KeysPage,
            "تعلم": LearnPage,
        }

        page_class = page_classes.get(page_name)
        if page_class is None:
            self.display_status(f"الصفحة غير موجودة: {page_name}", success=False)
            return

        self.active_page = page_class(self.content_frame, self)
        self.active_page.grid(row=0, column=0, sticky="nsew")
        self.display_status(f"تم تحميل صفحة {page_name}", success=True)

    def display_status(self, message: str, success: bool = True):
        """Show a friendly message in the bottom status bar."""
        color = "#5ee4b8" if success else "#ff6b6b"
        self.status_label.configure(text=message, text_color=color)


if __name__ == "__main__":
    app = CryptoLabApp()
    app.mainloop()
