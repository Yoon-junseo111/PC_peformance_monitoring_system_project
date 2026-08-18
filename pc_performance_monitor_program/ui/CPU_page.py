import customtkinter as ctk


# ==================================================
# CPU 상세 페이지
# ==================================================

class CPUPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)


        # 페이지 제목
        title = ctk.CTkLabel(
            self,
            text="CPU",
            font=("Arial", 30, "bold")
        )

        title.pack(
            anchor="w",
            padx=30,
            pady=30
        )


        # 나중에 CPU 상세 정보와
        # CPU 전용 그래프를 추가할 영역
        info = ctk.CTkLabel(
            self,
            text="CPU 상세 정보가 표시될 페이지입니다.",
            font=("Arial", 16)
        )

        info.pack(
            padx=30,
            pady=20
        )
        
        