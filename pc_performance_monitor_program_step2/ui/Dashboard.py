# ==================================================
# 라이브러리
# ==================================================

import customtkinter as ctk

# monitor.py에서 하드웨어 정보 함수 가져오기
from monitor import get_cpu_info
from monitor import get_gpu_info
from monitor import get_ram_info


# ==================================================
# Dashboard 페이지
# ==================================================

class DashboardPage(ctk.CTkFrame):

    def __init__(self, parent):

        # 부모 Frame 초기화
        super().__init__(parent)


        # ==================================================
        # 제목
        # ==================================================

        title = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=("Arial", 30, "bold")
        )

        title.pack(
            anchor="w",
            padx=30,
            pady=(30, 20)
        )


        # ==================================================
        # 카드들을 담을 Frame
        # ==================================================

        cards_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        cards_frame.pack(
            fill="x",
            padx=20
        )


        # CPU / GPU / RAM이 같은 크기가 되도록 설정
        cards_frame.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )


        # ==================================================
        # CPU 카드
        # ==================================================

        cpu_card = ctk.CTkFrame(
            cards_frame,
            corner_radius=15
        )

        cpu_card.grid(
            row=0,
            column=0,
            padx=10,
            sticky="nsew"
        )


        cpu_title = ctk.CTkLabel(
            cpu_card,
            text="CPU",
            font=("Arial", 18, "bold")
        )

        cpu_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        self.cpu_value = ctk.CTkLabel(
            cpu_card,
            text="0%",
            font=("Arial", 35, "bold")
        )

        self.cpu_value.pack(
            anchor="w",
            padx=20
        )


        self.cpu_progress = ctk.CTkProgressBar(
            cpu_card
        )

        self.cpu_progress.pack(
            fill="x",
            padx=20,
            pady=20
        )


        # ==================================================
        # GPU 카드
        # ==================================================

        gpu_card = ctk.CTkFrame(
            cards_frame,
            corner_radius=15
        )

        gpu_card.grid(
            row=0,
            column=1,
            padx=10,
            sticky="nsew"
        )


        gpu_title = ctk.CTkLabel(
            gpu_card,
            text="GPU",
            font=("Arial", 18, "bold")
        )

        gpu_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        self.gpu_value = ctk.CTkLabel(
            gpu_card,
            text="0%",
            font=("Arial", 35, "bold")
        )

        self.gpu_value.pack(
            anchor="w",
            padx=20
        )


        self.gpu_progress = ctk.CTkProgressBar(
            gpu_card
        )

        self.gpu_progress.pack(
            fill="x",
            padx=20,
            pady=20
        )


        # ==================================================
        # RAM 카드
        # ==================================================

        ram_card = ctk.CTkFrame(
            cards_frame,
            corner_radius=15
        )

        ram_card.grid(
            row=0,
            column=2,
            padx=10,
            sticky="nsew"
        )


        ram_title = ctk.CTkLabel(
            ram_card,
            text="RAM",
            font=("Arial", 18, "bold")
        )

        ram_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        self.ram_value = ctk.CTkLabel(
            ram_card,
            text="0%",
            font=("Arial", 35, "bold")
        )

        self.ram_value.pack(
            anchor="w",
            padx=20
        )


        self.ram_progress = ctk.CTkProgressBar(
            ram_card
        )

        self.ram_progress.pack(
            fill="x",
            padx=20,
            pady=20
        )


        # ==================================================
        # 데이터 업데이트 시작
        # ==================================================

        self.update_info()


    # ==================================================
    # 실시간 데이터 업데이트
    # ==================================================

    def update_info(self):

        # monitor.py에서 정보 가져오기
        cpu = get_cpu_info()
        gpu = get_gpu_info()
        ram = get_ram_info()


        # CPU 사용률 표시
        self.cpu_value.configure(
            text=f"{cpu['usage']:.0f}%"
        )

        # ProgressBar는 0 ~ 1 사이 값 사용
        self.cpu_progress.set(
            cpu["usage"] / 100
        )


        # GPU 사용률 표시
        self.gpu_value.configure(
            text=f"{gpu['usage']}%"
        )

        self.gpu_progress.set(
            gpu["usage"] / 100
        )


        # RAM 사용률 표시
        self.ram_value.configure(
            text=f"{ram['usage']:.0f}%"
        )

        self.ram_progress.set(
            ram["usage"] / 100
        )


        # 1000ms = 1초 후 다시 실행
        self.after(
            1000,
            self.update_info
        )