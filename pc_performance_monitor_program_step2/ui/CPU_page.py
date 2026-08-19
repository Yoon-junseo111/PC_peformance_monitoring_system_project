# ==================================================
# 필요한 라이브러리 불러오기
# ==================================================

# CustomTkinter:
# 일반 tkinter보다 조금 더 현대적인 UI를 만들기 쉬운 라이브러리
import customtkinter as ctk

# matplotlib의 Figure 클래스
# 실시간 CPU 사용률 그래프를 만들기 위해 사용
from matplotlib.figure import Figure

# matplotlib 그래프를 Tkinter / CustomTkinter 안에 넣기 위한 기능
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# monitor.py에 만들어둔 CPU 정보 함수 불러오기
# get_cpu_info()는 CPU 이름, 사용률, 물리 코어 수, 논리 코어 수 등을 반환한다고 가정
from monitor import get_cpu_info


# ==================================================
# CPU 페이지 클래스
# ==================================================

# CTkFrame을 상속받아서
# 하나의 독립적인 CPU 상세 페이지를 만듦
class CPUPage(ctk.CTkFrame):

    def __init__(self, parent):

        # 부모 CTkFrame 초기화
        # parent에는 main.py의 page_container가 들어오게 됨
        super().__init__(parent)


        # ==================================================
        # 실시간 그래프용 데이터
        # ==================================================

        # X축에 사용할 시간 값 저장
        # 예:
        # [0, 1, 2, 3, 4 ...]
        self.time_data = []

        # Y축에 사용할 CPU 사용률 저장
        # 예:
        # [15, 30, 45, 22 ...]
        self.cpu_data = []

        # 그래프에 표시할 데이터 개수
        # 최근 30개의 데이터만 유지
        self.max_data = 30

        # 1초마다 증가하는 시간 카운터
        self.counter = 0


        # ==================================================
        # CPU 페이지 제목
        # ==================================================

        title = ctk.CTkLabel(
            self,
            text="CPU",
            font=("Arial", 30, "bold")
        )

        title.pack(
            anchor="w",
            padx=30,
            pady=(30, 10)
        )


        # ==================================================
        # CPU 이름 표시
        # ==================================================

        # 처음 실행했을 때는 아직 CPU 정보를 읽기 전이므로
        # 임시 문구를 표시
        self.cpu_name_label = ctk.CTkLabel(
            self,
            text="CPU 정보를 불러오는 중...",
            font=("Arial", 16)
        )

        self.cpu_name_label.pack(
            anchor="w",
            padx=30,
            pady=(0, 20)
        )


        # ==================================================
        # CPU 정보 카드 영역
        # ==================================================

        # CPU Usage / Physical Cores / Logical Cores
        # 3개의 카드를 담는 Frame
        cards_frame = ctk.CTkFrame(
            self,

            # 부모 배경색을 그대로 사용
            fg_color="transparent"
        )

        cards_frame.pack(
            fill="x",
            padx=20
        )


        # 3개의 카드가 같은 비율로 넓어지도록 설정
        cards_frame.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )


        # ==================================================
        # CPU 사용률 카드
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
            text="CPU Usage",
            font=("Arial", 17, "bold")
        )

        usage_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        # CPU 사용률 숫자 표시
        # 예: 36%
        self.cpu_usage_label = ctk.CTkLabel(
            usage_card,
            text="0%",
            font=("Arial", 34, "bold")
        )

        self.cpu_usage_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )


        # ==================================================
        # 물리 코어 수 카드
        # ==================================================

        # 실제 CPU 안에 있는 물리적인 코어 개수
        # 예:
        # 6 Core CPU -> Physical Cores = 6
        physical_card = ctk.CTkFrame(
            cards_frame,
            corner_radius=15
        )

        physical_card.grid(
            row=0,
            column=1,
            padx=10,
            sticky="nsew"
        )


        physical_title = ctk.CTkLabel(
            physical_card,
            text="Physical Cores",
            font=("Arial", 17, "bold")
        )

        physical_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        self.physical_core_label = ctk.CTkLabel(
            physical_card,
            text="0",
            font=("Arial", 34, "bold")
        )

        self.physical_core_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )


        # ==================================================
        # 논리 코어 수 카드
        # ==================================================

        # 운영체제에서 인식하는 논리적인 CPU 개수
        # 하이퍼스레딩/SMT가 활성화되어 있으면
        # 물리 코어보다 많을 수 있음
        #
        # 예:
        # Physical = 8
        # Logical = 16
        logical_card = ctk.CTkFrame(
            cards_frame,
            corner_radius=15
        )

        logical_card.grid(
            row=0,
            column=2,
            padx=10,
            sticky="nsew"
        )


        logical_title = ctk.CTkLabel(
            logical_card,
            text="Logical Cores",
            font=("Arial", 17, "bold")
        )

        logical_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        self.logical_core_label = ctk.CTkLabel(
            logical_card,
            text="0",
            font=("Arial", 34, "bold")
        )

        self.logical_core_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )


        # ==================================================
        # CPU 사용률 Progress Bar 카드
        # ==================================================

        # CPU 사용률을 막대 형태로 보여주는 영역
        usage_progress_card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        usage_progress_card.pack(
            fill="x",
            padx=30,
            pady=(20, 10)
        )


        # 카드 제목
        progress_title = ctk.CTkLabel(
            usage_progress_card,
            text="CPU Load",
            font=("Arial", 17, "bold")
        )

        progress_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        # CPU 사용률 텍스트
        self.cpu_progress_text = ctk.CTkLabel(
            usage_progress_card,
            text="0%",
            font=("Arial", 20, "bold")
        )

        self.cpu_progress_text.pack(
            anchor="w",
            padx=20
        )


        # ==================================================
        # CPU 사용률 Progress Bar
        # ==================================================

        self.cpu_progress = ctk.CTkProgressBar(
            usage_progress_card
        )

        self.cpu_progress.pack(
            fill="x",
            padx=20,
            pady=20
        )

        # 시작 값 0%
        self.cpu_progress.set(0)


        # ==================================================
        # 실시간 그래프 영역
        # ==================================================

        graph_frame = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        # fill="both":
        # 가로와 세로 모두 늘어나도록 설정
        #
        # expand=True:
        # 남는 공간을 그래프가 사용
        graph_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(10, 30)
        )


        # ==================================================
        # matplotlib Figure 생성
        # ==================================================

        # Figure는 그래프 전체 틀
        self.figure = Figure(
            figsize=(8, 4),
            dpi=100
        )

        # 하나의 그래프 영역 생성
        self.ax = self.figure.add_subplot(111)


        # ==================================================
        # 그래프 기본 설정
        # ==================================================

        # 그래프 제목
        self.ax.set_title(
            "CPU Real-time Usage"
        )

        # CPU 사용률은 0~100%
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

            # 그래프가 들어갈 부모 Frame
            master=graph_frame
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )


        # ==================================================
        # CPU 정보 실시간 업데이트 시작
        # ==================================================

        # CPU 페이지가 만들어지는 순간부터
        # CPU 정보를 계속 읽어오기 시작
        self.update_cpu_info()


    # ==================================================
    # CPU 정보를 1초마다 갱신하는 함수
    # ==================================================

    def update_cpu_info(self):

        # monitor.py의 get_cpu_info() 호출
        #
        # 예:
        #
        # {
        #     "name": "Intel(R) Core(TM) i7-12700K",
        #     "usage": 35.2,
        #     "physical_cores": 12,
        #     "logical_cores": 20
        # }
        cpu = get_cpu_info()


        # ==================================================
        # CPU 이름 업데이트
        # ==================================================

        self.cpu_name_label.configure(
            text=cpu["name"]
        )


        # ==================================================
        # CPU 사용률 업데이트
        # ==================================================

        # 사용률을 소수점 첫째 자리까지 표시
        #
        # 예:
        # 34.8%
        self.cpu_usage_label.configure(
            text=f"{cpu['usage']:.1f}%"
        )


        # ==================================================
        # 물리 코어 수 업데이트
        # ==================================================

        self.physical_core_label.configure(
            text=str(cpu["physical_cores"])
        )


        # ==================================================
        # 논리 코어 수 업데이트
        # ==================================================

        self.logical_core_label.configure(
            text=str(cpu["logical_cores"])
        )


        # ==================================================
        # CPU Progress Bar 텍스트 업데이트
        # ==================================================

        self.cpu_progress_text.configure(
            text=f"{cpu['usage']:.1f}%"
        )


        # ==================================================
        # CPU Progress Bar 업데이트
        # ==================================================

        # CPU 사용률은 0 ~ 100
        #
        # CustomTkinter ProgressBar는
        # 0.0 ~ 1.0 값을 사용
        #
        # 따라서 100으로 나눔
        #
        # 예:
        # CPU 50%
        # 50 / 100 = 0.5
        self.cpu_progress.set(
            cpu["usage"] / 100
        )


        # ==================================================
        # 그래프 데이터 저장
        # ==================================================

        # 현재 시간을 X축에 추가
        self.time_data.append(
            self.counter
        )

        # 현재 CPU 사용률을 Y축에 추가
        self.cpu_data.append(
            cpu["usage"]
        )


        # ==================================================
        # 시간 카운터 증가
        # ==================================================

        # update_cpu_info()가 호출될 때마다
        # 1씩 증가
        #
        # 1초마다 실행되므로
        # 거의 초 단위 시간처럼 사용할 수 있음
        self.counter += 1


        # ==================================================
        # 최근 30개 데이터만 유지
        # ==================================================

        # 30개를 초과하면
        # 가장 오래된 데이터 삭제
        #
        # 이렇게 하지 않으면 프로그램을 오래 실행할수록
        # 리스트가 계속 커지게 됨
        if len(self.time_data) > self.max_data:

            # 가장 오래된 시간 제거
            self.time_data.pop(0)

            # 가장 오래된 CPU 사용률 제거
            self.cpu_data.pop(0)


        # ==================================================
        # 기존 그래프 초기화
        # ==================================================

        # 새 데이터를 그리기 전에
        # 기존 그래프를 제거
        self.ax.clear()


        # ==================================================
        # clear() 후 그래프 설정 다시 적용
        # ==================================================

        # clear()를 하면
        # 제목, 축, 격자 등도 전부 사라지므로
        # 다시 설정해야 함

        self.ax.set_title(
            "CPU Real-time Usage"
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
        # CPU 실시간 그래프 그리기
        # ==================================================

        self.ax.plot(
            self.time_data,
            self.cpu_data,

            # 범례에 표시할 이름
            label="CPU",

            # 선 두께
            linewidth=2
        )


        # 그래프 범례 표시
        self.ax.legend()


        # ==================================================
        # 그래프 화면 갱신
        # ==================================================

        self.canvas.draw()


        # ==================================================
        # 1초 후 다시 update_cpu_info 실행
        # ==================================================

        # after()는 GUI를 멈추지 않고
        # 일정 시간이 지난 뒤 함수를 다시 실행하게 함
        #
        # 1000ms = 1초
        self.after(
            1000,
            self.update_cpu_info
        )