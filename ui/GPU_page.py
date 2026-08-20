# ==================================================
# 필요한 라이브러리 불러오기
# ==================================================

# CustomTkinter:
# tkinter보다 조금 더 현대적인 디자인을 쉽게 만들 수 있는 라이브러리
import customtkinter as ctk

# matplotlib의 Figure:
# 그래프 전체 틀을 만들기 위해 사용
from matplotlib.figure import Figure

# matplotlib 그래프를 Tkinter / CustomTkinter 안에 넣기 위한 클래스
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# monitor.py에서 GPU 정보를 가져오는 함수
# 이 함수는 GPU 이름, 사용률, 온도, VRAM 정보를 dictionary 형태로 반환한다고 가정
from monitor import get_gpu_info


# ==================================================
# GPU 페이지 클래스
# ==================================================

# CTkFrame을 상속받아서
# 하나의 "페이지"처럼 사용할 수 있는 Frame을 생성
class GPUPage(ctk.CTkFrame):

    def __init__(self, parent):

        # 부모 클래스인 CTkFrame의 초기화 실행
        # parent는 main.py의 page_container가 들어오게 됨
        super().__init__(parent)


        # ==================================================
        # 그래프에서 사용할 데이터 저장 공간
        # ==================================================

        # X축에 사용할 시간 데이터
        # 예: [0, 1, 2, 3, 4 ...]
        self.time_data = []

        # Y축에 사용할 GPU 사용률 데이터
        # 예: [20, 30, 45, 25 ...]
        self.gpu_data = []

        # 그래프에 너무 많은 데이터가 쌓이지 않도록
        # 최근 30개의 데이터만 유지
        self.max_data = 30

        # 시간이 흐르는 것을 표현하기 위한 숫자
        # 1초마다 1씩 증가
        self.counter = 0


        # ==================================================
        # 페이지 제목
        # ==================================================

        # GPU 페이지의 가장 위쪽 제목
        title = ctk.CTkLabel(
            self,

            # 화면에 표시할 글자
            text="GPU",

            # 글꼴 설정
            # Arial, 크기 30, 굵게
            font=("Arial", 30, "bold")
        )

        # pack을 사용해서 위쪽에 배치
        title.pack(
            anchor="w",          # 왼쪽 정렬
            padx=30,             # 좌우 여백
            pady=(30, 10)        # 위 30, 아래 10
        )


        # ==================================================
        # GPU 이름 표시
        # ==================================================

        # 처음 실행했을 때 GPU 정보를 아직 못 가져왔기 때문에
        # "불러오는 중..."이라는 문장을 먼저 표시
        self.gpu_name_label = ctk.CTkLabel(
            self,
            text="GPU 정보를 불러오는 중...",
            font=("Arial", 16)
        )

        self.gpu_name_label.pack(
            anchor="w",
            padx=30,
            pady=(0, 20)
        )


        # ==================================================
        # GPU 사용률 / 온도 카드 영역
        # ==================================================

        # GPU 사용률 카드와 온도 카드를 담을 Frame
        # fg_color="transparent"를 사용하면
        # 부모 배경색을 그대로 사용
        cards_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        # 화면 가로 길이만큼 늘어나도록 fill="x"
        cards_frame.pack(
            fill="x",
            padx=20
        )


        # ==================================================
        # Grid column 설정
        # ==================================================

        # 카드 두 개를 0번, 1번 column에 배치할 예정
        # 두 column의 weight를 동일하게 1로 설정하면
        # 두 카드가 같은 비율로 넓어짐
        cards_frame.grid_columnconfigure(
            (0, 1),
            weight=1
        )


        # ==================================================
        # GPU 사용률 카드
        # ==================================================

        # GPU 사용률을 보여줄 카드 생성
        usage_card = ctk.CTkFrame(
            cards_frame,

            # 카드 모서리를 둥글게
            corner_radius=15
        )

        # grid를 사용해서 첫 번째 칸에 배치
        usage_card.grid(
            row=0,
            column=0,

            # 카드 사이 간격
            padx=10,

            # 카드가 칸 전체를 채우도록
            sticky="nsew"
        )


        # GPU Usage 제목
        usage_title = ctk.CTkLabel(
            usage_card,
            text="GPU Usage",
            font=("Arial", 17, "bold")
        )

        usage_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        # ==================================================
        # GPU 사용률 숫자
        # ==================================================

        # 실제 GPU 사용률을 큰 숫자로 표시
        # 예: 35%
        self.gpu_usage_label = ctk.CTkLabel(
            usage_card,

            # 처음에는 0%
            text="0%",

            # 숫자가 잘 보이도록 크게 설정
            font=("Arial", 36, "bold")
        )

        self.gpu_usage_label.pack(
            anchor="w",
            padx=20
        )


        # ==================================================
        # GPU 사용률 Progress Bar
        # ==================================================

        # 사용률을 막대 형태로 표시
        self.gpu_progress = ctk.CTkProgressBar(
            usage_card
        )

        self.gpu_progress.pack(
            fill="x",
            padx=20,
            pady=20
        )

        # CTkProgressBar는
        # 0.0 ~ 1.0 사이 값을 사용함
        # 처음에는 0으로 설정
        self.gpu_progress.set(0)


        # ==================================================
        # GPU 온도 카드
        # ==================================================

        # GPU 온도를 보여줄 카드
        temperature_card = ctk.CTkFrame(
            cards_frame,
            corner_radius=15
        )

        # 두 번째 칸에 배치
        temperature_card.grid(
            row=0,
            column=1,
            padx=10,
            sticky="nsew"
        )


        # 온도 카드 제목
        temperature_title = ctk.CTkLabel(
            temperature_card,
            text="Temperature",
            font=("Arial", 17, "bold")
        )

        temperature_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        # ==================================================
        # GPU 온도 숫자
        # ==================================================

        # 예: 65°C
        self.temperature_label = ctk.CTkLabel(
            temperature_card,
            text="0°C",
            font=("Arial", 36, "bold")
        )

        self.temperature_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )


        # ==================================================
        # VRAM 카드
        # ==================================================

        # GPU 메모리(VRAM) 정보를 보여주는 카드
        vram_card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        # GPU Usage / Temperature 카드 아래쪽에 배치
        vram_card.pack(
            fill="x",
            padx=30,
            pady=(20, 10)
        )


        # VRAM 제목
        vram_title = ctk.CTkLabel(
            vram_card,
            text="VRAM",
            font=("Arial", 17, "bold")
        )

        vram_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        # ==================================================
        # VRAM 사용량 표시
        # ==================================================

        # 예:
        # 3.25 GB / 8.00 GB
        self.vram_label = ctk.CTkLabel(
            vram_card,
            text="0 GB / 0 GB",
            font=("Arial", 20, "bold")
        )

        self.vram_label.pack(
            anchor="w",
            padx=20
        )


        # ==================================================
        # VRAM Progress Bar
        # ==================================================

        # VRAM 사용량을 막대로 표시
        self.vram_progress = ctk.CTkProgressBar(
            vram_card
        )

        self.vram_progress.pack(
            fill="x",
            padx=20,
            pady=20
        )

        self.vram_progress.set(0)


        # ==================================================
        # 그래프를 담을 Frame
        # ==================================================

        # 실시간 GPU 사용률 그래프가 들어갈 영역
        graph_frame = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        # fill="both":
        # 가로/세로 모두 늘어남
        #
        # expand=True:
        # 남은 공간까지 그래프 영역이 사용
        graph_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(10, 30)
        )


        # ==================================================
        # matplotlib 그래프 생성
        # ==================================================

        # Figure는 그래프 전체 종이라고 생각하면 됨
        self.figure = Figure(
            figsize=(8, 4),
            dpi=100
        )

        # 하나의 그래프 영역 생성
        # 111 의미:
        # 1행 / 1열 / 첫 번째 그래프
        self.ax = self.figure.add_subplot(111)


        # ==================================================
        # 그래프 기본 설정
        # ==================================================

        # 그래프 제목
        self.ax.set_title(
            "GPU Real-time Usage"
        )

        # GPU 사용률 범위는 0~100%
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

        # 배경 격자 표시
        self.ax.grid(
            True
        )


        # ==================================================
        # matplotlib 그래프를 CustomTkinter에 연결
        # ==================================================

        # FigureCanvasTkAgg를 사용하면
        # matplotlib Figure를 Tkinter Widget처럼 사용할 수 있음
        self.canvas = FigureCanvasTkAgg(
            self.figure,

            # 그래프가 들어갈 부모 Frame
            master=graph_frame
        )

        # 실제 그래프 Widget을 pack으로 배치
        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )


        # ==================================================
        # 실시간 정보 업데이트 시작
        # ==================================================

        # 페이지가 만들어지면 바로 GPU 정보를 읽기 시작
        self.update_gpu_info()


    # ==================================================
    # GPU 정보를 1초마다 갱신하는 함수
    # ==================================================

    def update_gpu_info(self):

        # monitor.py의 get_gpu_info() 실행
        #
        # 예:
        # {
        #     "name": "NVIDIA GeForce RTX 4060",
        #     "usage": 35,
        #     "temperature": 62,
        #     "vram_used": 3.25,
        #     "vram_total": 8.00
        # }
        gpu = get_gpu_info()


        # ==================================================
        # GPU 이름 갱신
        # ==================================================

        self.gpu_name_label.configure(
            text=gpu["name"]
        )


        # ==================================================
        # GPU 사용률 숫자 갱신
        # ==================================================

        # 예: 35%
        self.gpu_usage_label.configure(
            text=f"{gpu['usage']}%"
        )


        # ==================================================
        # GPU 사용률 Progress Bar 갱신
        # ==================================================

        # gpu["usage"]는 0~100 값
        #
        # ProgressBar는 0~1 값이 필요하므로
        # 100으로 나눠줌
        #
        # 예:
        # 35 / 100 = 0.35
        self.gpu_progress.set(
            gpu["usage"] / 100
        )


        # ==================================================
        # GPU 온도 갱신
        # ==================================================

        self.temperature_label.configure(
            text=f"{gpu['temperature']}°C"
        )


        # ==================================================
        # VRAM 사용량 텍스트 갱신
        # ==================================================

        # 소수점 둘째 자리까지 표시
        #
        # 예:
        # 3.25 GB / 8.00 GB
        self.vram_label.configure(
            text=(
                f"{gpu['vram_used']:.2f} GB / "
                f"{gpu['vram_total']:.2f} GB"
            )
        )


        # ==================================================
        # VRAM 사용률 계산
        # ==================================================

        # 0으로 나누는 오류를 방지하기 위해
        # 전체 VRAM이 0보다 큰지 먼저 확인
        if gpu["vram_total"] > 0:

            # VRAM 사용 비율 계산
            #
            # 예:
            # 4GB 사용 / 8GB 전체 = 0.5
            vram_percent = (
                gpu["vram_used"]
                / gpu["vram_total"]
            )

        else:

            # 혹시 전체 VRAM이 0으로 들어오면
            # Progress Bar를 0으로 유지
            vram_percent = 0


        # VRAM Progress Bar 갱신
        self.vram_progress.set(
            vram_percent
        )


        # ==================================================
        # 그래프 데이터 추가
        # ==================================================

        # 현재 시간 값을 X축 리스트에 추가
        self.time_data.append(
            self.counter
        )

        # 현재 GPU 사용률을 Y축 리스트에 추가
        self.gpu_data.append(
            gpu["usage"]
        )

        # 다음 업데이트를 위해 시간 1 증가
        self.counter += 1


        # ==================================================
        # 최근 30개 데이터만 유지
        # ==================================================

        # 데이터가 30개를 초과하면
        # 가장 오래된 데이터를 하나 제거
        if len(self.time_data) > self.max_data:

            self.time_data.pop(0)

            self.gpu_data.pop(0)


        # ==================================================
        # 기존 그래프 지우기
        # ==================================================

        # 매초 새로운 그래프를 다시 그리기 때문에
        # 기존 그래프를 먼저 초기화
        self.ax.clear()


        # ==================================================
        # 그래프 설정 다시 적용
        # ==================================================

        # clear()를 하면
        # 제목, 축 설정, 격자도 모두 사라지기 때문에
        # 다시 설정해야 함

        self.ax.set_title(
            "GPU Real-time Usage"
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
        # GPU 사용률 선 그래프 그리기
        # ==================================================

        self.ax.plot(
            self.time_data,
            self.gpu_data,

            # 범례에 표시할 이름
            label="GPU",

            # 선 두께
            linewidth=2
        )

        # 범례 표시
        self.ax.legend()


        # ==================================================
        # 화면에 그래프 다시 그리기
        # ==================================================

        self.canvas.draw()


        # ==================================================
        # 1초 후 update_gpu_info 다시 실행
        # ==================================================

        # after(1000, 함수)
        #
        # 1000ms = 1초
        #
        # 따라서 GPU 정보가 1초마다 계속 갱신됨
        self.after(
            1000,
            self.update_gpu_info
        )