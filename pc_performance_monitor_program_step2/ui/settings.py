import customtkinter as ctk


class SettingsPage(ctk.CTkFrame):

    def __init__(self, parent):

        # 부모 Frame 초기화
        super().__init__(parent)

        # Settings 페이지 제목
        title = ctk.CTkLabel(
            self,
            text="Settings",
            font=("Arial", 30, "bold")
        )

        title.pack(
            anchor="w",
            padx=30,
            pady=30
        )