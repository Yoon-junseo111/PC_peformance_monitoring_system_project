# ==================================================
# 필요한 라이브러리 불러오기
# ==================================================

# 앱 UI를 만들기 위한 CustomTkinter
import customtkinter as ctk

# matplotlib 그래프 틀
from matplotlib.figure import Figure

# matplotlib 그래프를 Tkinter 안에 넣기 위한 클래스
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# monitor.py에서 RAM 정보 가져오기
from monitor import get_ram_info


# ==================================================
# RAM 페이지 클래스
# ==================================================

class RAMPage(ctk.CTkFrame):

    def __init__(self, parent):

        # CTkFrame 초기화
        super().__init__(parent)


        # ==================================================
        # 그래프용 데이터
        # ==================================================

        # X축 시간 값 저장
        self.time_data = []

        # Y축 RAM 사용률 저장
        self.ram_data = []

        # 최근 데이터 30개만 그래프에 표시
        self.max_data = 30

        # 시간 증가용 숫자
        self.counter = 0


        # ==================================================
        # RAM 페이지 제목
        # ==================================================

        title = ctk.CTkLabel(
            self,
            text="RAM",
            font=("Arial", 30, "bold")
        )

        title.pack(
            anchor="w",
            padx=30,
            pady=(30, 20)
        )


        # ==================================================
        # 상단 카드 영역
        # ==================================================

        # RAM Usage / Used / Available
        # 총 3개의 카드를 담는 Frame
        cards_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        cards_frame.pack(
            fill="x",
            padx=20
        )


        # 3개의 카드가 동일한 크기로 배치되도록 설정
        cards_frame.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )


        # ==================================================
        # RAM 사용률 카드
        # ==================================================

        usage_card = ctk.CTkFrame(
            cards_frame,
            corner_radius=15
        )

        usage_card.grid(
            row=0,
            column=0,
            padx=10,
            sticky="nsew"
        )


        # 카드 제목
        usage_title = ctk.CTkLabel(
            usage_card,
            text="RAM Usage",
            font=("Arial", 17, "bold")
        )

        usage_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        # RAM 사용률 숫자
        # 예: 52.4%
        self.ram_usage_label = ctk.CTkLabel(
            usage_card,
            text="0%",
            font=("Arial", 34, "bold")
        )

        self.ram_usage_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )


        # ==================================================
        # 사용 중인 RAM 카드
        # ==================================================

        used_card = ctk.CTkFrame(
            cards_frame,
            corner_radius=15
        )

        used_card.grid(
            row=0,
            column=1,
            padx=10,
            sticky="nsew"
        )


        # 카드 제목
        used_title = ctk.CTkLabel(
            used_card,
            text="Used",
            font=("Arial", 17, "bold")
        )

        used_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        # 실제 사용 중인 RAM 용량
        # 예: 9.82 GB
        self.used_label = ctk.CTkLabel(
            used_card,
            text="0 GB",
            font=("Arial", 30, "bold")
        )

        self.used_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )


        # ==================================================
        # 사용 가능한 RAM 카드
        # ==================================================

        available_card = ctk.CTkFrame(
            cards_frame,
            corner_radius=15
        )

        available_card.grid(
            row=0,
            column=2,
            padx=10,
            sticky="nsew"
        )


        # 카드 제목
        available_title = ctk.CTkLabel(
            available_card,
            text="Available",
            font=("Arial", 17, "bold")
        )

        available_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        # 사용 가능한 RAM 용량
        # 예: 6.11 GB
        self.available_label = ctk.CTkLabel(
            available_card,
            text="0 GB",
            font=("Arial", 30, "bold")
        )

        self.available_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )


        # ==================================================
        # 전체 RAM 상태 카드
        # ==================================================

        # 사용량 / 전체 용량 및 Progress Bar를 표시
        memory_card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        memory_card.pack(
            fill="x",
            padx=30,
            pady=(20, 10)
        )


        # 카드 제목
        memory_title = ctk.CTkLabel(
            memory_card,
            text="Memory",
            font=("Arial", 17, "bold")
        )

        memory_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        # ==================================================
        # RAM 사용량 / 전체 용량
        # ==================================================

        # 예:
        # 9.82 GB / 16.00 GB
        self.memory_label = ctk.CTkLabel(
            memory_card,
            text="0 GB / 0 GB",
            font=("Arial", 20, "bold")
        )

        self.memory_label.pack(
            anchor="w",
            padx=20
        )


        # ==================================================
        # RAM 사용률 Progress Bar
        # ==================================================

        self.ram_progress = ctk.CTkProgressBar(
            memory_card
        )

        self.ram_progress.pack(
            fill="x",
            padx=20,
            pady=20
        )

        # 시작 값은 0
        self.ram_progress.set(0)


        # ==================================================
        # 실시간 그래프 영역
        # ==================================================

        graph_frame = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        graph_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(10, 30)
        )


        # ==================================================
        # matplotlib Figure 생성
        # ==================================================

        self.figure = Figure(
            figsize=(8, 4),
            dpi=100
        )

        # 그래프 하나 생성
        self.ax = self.figure.add_subplot(111)


        # ==================================================
        # 그래프 기본 설정
        # ==================================================

        # 그래프 제목
        self.ax.set_title(
            "RAM Real-time Usage"
        )

        # RAM 사용률 범위는 0~100%
        self.ax.set_ylim(
            0,
            100
        )

        # Y축 이름
        self.ax.set_ylabel(
            "Usage (%)"
        )

        # X축 이름
        self.ax.set_xlabel(
            "Time"
        )

        # 격자 표시
        self.ax.grid(
            True
        )


        # ==================================================
        # matplotlib 그래프를 CustomTkinter에 넣기
        # ==================================================

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=graph_frame
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )


        # ==================================================
        # 실시간 RAM 정보 업데이트 시작
        # ==================================================

        self.update_ram_info()


    # ==================================================
    # RAM 정보를 1초마다 가져오는 함수
    # ==================================================

    def update_ram_info(self):

        # monitor.py에서 RAM 정보 가져오기
        #
        # 예:
        # {
        #     "usage": 52.4,
        #     "total": 16.0,
        #     "used": 9.5,
        #     "available": 6.5
        # }
        ram = get_ram_info()


        # ==================================================
        # RAM 사용률 숫자 갱신
        # ==================================================

        self.ram_usage_label.configure(
            text=f"{ram['usage']:.1f}%"
        )


        # ==================================================
        # 사용 중 RAM 갱신
        # ==================================================

        self.used_label.configure(
            text=f"{ram['used']:.2f} GB"
        )


        # ==================================================
        # 사용 가능한 RAM 갱신
        # ==================================================

        self.available_label.configure(
            text=f"{ram['available']:.2f} GB"
        )


        # ==================================================
        # 사용량 / 전체 용량 표시
        # ==================================================

        self.memory_label.configure(
            text=(
                f"{ram['used']:.2f} GB / "
                f"{ram['total']:.2f} GB"
            )
        )


        # ==================================================
        # RAM Progress Bar 갱신
        # ==================================================

        # ram["usage"]는 0~100
        # Progress Bar는 0~1
        #
        # 따라서 100으로 나눔
        self.ram_progress.set(
            ram["usage"] / 100
        )


        # ==================================================
        # 그래프용 데이터 추가
        # ==================================================

        # 현재 시간값 추가
        self.time_data.append(
            self.counter
        )

        # 현재 RAM 사용률 추가
        self.ram_data.append(
            ram["usage"]
        )

        # 시간 1 증가
        self.counter += 1


        # ==================================================
        # 최근 30개의 데이터만 유지
        # ==================================================

        # 너무 많은 데이터가 쌓이면
        # 가장 오래된 데이터를 삭제
        if len(self.time_data) > self.max_data:

            self.time_data.pop(0)

            self.ram_data.pop(0)


        # ==================================================
        # 기존 그래프 제거
        # ==================================================

        # 새로운 데이터를 다시 그리기 위해 초기화
        self.ax.clear()


        # ==================================================
        # clear 후 그래프 설정 다시 적용
        # ==================================================

        self.ax.set_title(
            "RAM Real-time Usage"
        )

        self.ax.set_ylim(
            0,
            100
        )

        self.ax.set_ylabel(
            "Usage (%)"
        )

        self.ax.set_xlabel(
            "Time"
        )

        self.ax.grid(
            True
        )


        # ==================================================
        # RAM 사용률 선 그래프 그리기
        # ==================================================

        self.ax.plot(
            self.time_data,
            self.ram_data,
            label="RAM",
            linewidth=2
        )

        # 그래프 범례 표시
        self.ax.legend()


        # ==================================================
        # 그래프 화면 갱신
        # ==================================================

        self.canvas.draw()


        # ==================================================
        # 1초 후 update_ram_info 다시 호출
        # ==================================================

        # 이렇게 자기 자신을 계속 예약하기 때문에
        # 실시간 모니터처럼 계속 데이터가 바뀜
        self.after(
            1000,
            self.update_ram_info
        )