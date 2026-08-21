# ==================================================
# 필요한 라이브러리 불러오기
# ==================================================

# CustomTkinter UI
import customtkinter as ctk

# 시간 계산용
import time

# matplotlib 그래프
from matplotlib.figure import Figure

# matplotlib 그래프를 Tkinter 안에 넣기 위한 기능
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# monitor.py에서 Disk 정보 가져오기
from monitor import get_disk_info

# 공용 설정값 가져오기
import config


# ==================================================
# Disk 페이지 클래스
# ==================================================

class DiskPage(ctk.CTkFrame):

    def __init__(self, parent):

        # 부모 Frame 초기화
        super().__init__(parent)


        # ==================================================
        # 그래프 데이터 저장 공간
        # ==================================================

        # X축 시간 데이터
        self.time_data = []

        # Disk 읽기 속도 데이터
        self.read_data = []

        # Disk 쓰기 속도 데이터
        self.write_data = []

        # 시간 증가용 카운터
        self.counter = 0


        # ==================================================
        # Disk 속도 계산을 위한 이전 값
        # ==================================================

        # get_disk_info()에서 가져오는 read_bytes와 write_bytes는
        # 현재 속도가 아니라 Windows 부팅 이후 누적된 값임
        #
        # 따라서 이전 값과 현재 값의 차이를 계산해야
        # MB/s 단위의 실제 속도를 구할 수 있음

        first_disk_info = get_disk_info()

        # 처음 읽어온 누적 읽기 Byte 저장
        self.previous_read_bytes = first_disk_info["read_bytes"]

        # 처음 읽어온 누적 쓰기 Byte 저장
        self.previous_write_bytes = first_disk_info["write_bytes"]

        # 처음 측정한 시간 저장
        self.previous_time = time.time()


        # ==================================================
        # 페이지 제목
        # ==================================================

        title = ctk.CTkLabel(
            self,
            text="Disk",
            font=("Arial", 30, "bold")
        )

        title.pack(
            anchor="w",
            padx=30,
            pady=(30, 10)
        )


        # ==================================================
        # Disk 이름
        # ==================================================

        disk_name = ctk.CTkLabel(
            self,
            text="C: Drive",
            font=("Arial", 16)
        )

        disk_name.pack(
            anchor="w",
            padx=30,
            pady=(0, 20)
        )


        # ==================================================
        # 상단 카드 영역
        # ==================================================

        # Total / Used / Free
        # 세 개의 정보를 카드로 표시
        cards_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        cards_frame.pack(
            fill="x",
            padx=20
        )


        # 세 개의 카드가 같은 크기로 보이도록 설정
        cards_frame.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )


        # ==================================================
        # Total Disk 카드
        # ==================================================

        total_card = ctk.CTkFrame(
            cards_frame,
            corner_radius=15
        )

        total_card.grid(
            row=0,
            column=0,
            padx=10,
            sticky="nsew"
        )


        total_title = ctk.CTkLabel(
            total_card,
            text="Total",
            font=("Arial", 17, "bold")
        )

        total_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        self.total_label = ctk.CTkLabel(
            total_card,
            text="0 GB",
            font=("Arial", 30, "bold")
        )

        self.total_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )


        # ==================================================
        # Used Disk 카드
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
        # Free Disk 카드
        # ==================================================

        free_card = ctk.CTkFrame(
            cards_frame,
            corner_radius=15
        )

        free_card.grid(
            row=0,
            column=2,
            padx=10,
            sticky="nsew"
        )


        free_title = ctk.CTkLabel(
            free_card,
            text="Free",
            font=("Arial", 17, "bold")
        )

        free_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        self.free_label = ctk.CTkLabel(
            free_card,
            text="0 GB",
            font=("Arial", 30, "bold")
        )

        self.free_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )


        # ==================================================
        # Disk Usage 카드
        # ==================================================

        usage_card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        usage_card.pack(
            fill="x",
            padx=30,
            pady=(20, 10)
        )


        usage_title = ctk.CTkLabel(
            usage_card,
            text="Disk Usage",
            font=("Arial", 17, "bold")
        )

        usage_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        # Disk 사용률 숫자
        self.disk_usage_label = ctk.CTkLabel(
            usage_card,
            text="0%",
            font=("Arial", 22, "bold")
        )

        self.disk_usage_label.pack(
            anchor="w",
            padx=20
        )


        # Disk 사용률 Progress Bar
        self.disk_progress = ctk.CTkProgressBar(
            usage_card
        )

        self.disk_progress.pack(
            fill="x",
            padx=20,
            pady=20
        )

        self.disk_progress.set(0)


        # ==================================================
        # Read / Write 속도 카드 영역
        # ==================================================

        speed_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        speed_frame.pack(
            fill="x",
            padx=20,
            pady=(10, 0)
        )


        # 두 카드 같은 크기로 설정
        speed_frame.grid_columnconfigure(
            (0, 1),
            weight=1
        )


        # ==================================================
        # Read Speed 카드
        # ==================================================

        read_card = ctk.CTkFrame(
            speed_frame,
            corner_radius=15
        )

        read_card.grid(
            row=0,
            column=0,
            padx=10,
            sticky="nsew"
        )


        read_title = ctk.CTkLabel(
            read_card,
            text="Read Speed",
            font=("Arial", 17, "bold")
        )

        read_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        self.read_speed_label = ctk.CTkLabel(
            read_card,
            text="0.00 MB/s",
            font=("Arial", 28, "bold")
        )

        self.read_speed_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )


        # ==================================================
        # Write Speed 카드
        # ==================================================

        write_card = ctk.CTkFrame(
            speed_frame,
            corner_radius=15
        )

        write_card.grid(
            row=0,
            column=1,
            padx=10,
            sticky="nsew"
        )


        write_title = ctk.CTkLabel(
            write_card,
            text="Write Speed",
            font=("Arial", 17, "bold")
        )

        write_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        self.write_speed_label = ctk.CTkLabel(
            write_card,
            text="0.00 MB/s",
            font=("Arial", 28, "bold")
        )

        self.write_speed_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )


        # ==================================================
        # 그래프 영역
        # ==================================================

        graph_frame = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        graph_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(20, 30)
        )


        # ==================================================
        # matplotlib 그래프 생성
        # ==================================================

        self.figure = Figure(
            figsize=(8, 4),
            dpi=100
        )

        self.ax = self.figure.add_subplot(111)


        # 그래프 기본 설정
        self.ax.set_title(
            "Disk Read / Write Speed"
        )

        self.ax.set_ylabel(
            "MB/s"
        )

        self.ax.set_xlabel(
            "Time"
        )

        self.ax.grid(
            True
        )


        # ==================================================
        # matplotlib 그래프를 CustomTkinter에 연결
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
        # 실시간 업데이트 시작
        # ==================================================

        self.update_disk_info()


    # ==================================================
    # Disk 정보 실시간 업데이트 함수
    # ==================================================

    def update_disk_info(self):

        # 현재 Disk 정보 가져오기
        disk = get_disk_info()


        # ==================================================
        # Disk 용량 정보 표시
        # ==================================================

        # 전체 용량
        self.total_label.configure(
            text=f"{disk['total']:.2f} GB"
        )

        # 사용 중인 용량
        self.used_label.configure(
            text=f"{disk['used']:.2f} GB"
        )

        # 남은 용량
        self.free_label.configure(
            text=f"{disk['free']:.2f} GB"
        )


        # ==================================================
        # Disk 사용률
        # ==================================================

        self.disk_usage_label.configure(
            text=f"{disk['percent']:.1f}%"
        )

        # Progress Bar는 0 ~ 1 사이 값 사용
        self.disk_progress.set(
            disk["percent"] / 100
        )


        # ==================================================
        # 현재 시간 가져오기
        # ==================================================

        current_time = time.time()


        # 이전 측정 시간과 현재 측정 시간 차이 계산
        elapsed_time = (
            current_time
            - self.previous_time
        )


        # ==================================================
        # Read / Write Byte 차이 계산
        # ==================================================

        # 현재 누적 읽기 값 - 이전 누적 읽기 값
        read_difference = (
            disk["read_bytes"]
            - self.previous_read_bytes
        )

        # 현재 누적 쓰기 값 - 이전 누적 쓰기 값
        write_difference = (
            disk["write_bytes"]
            - self.previous_write_bytes
        )


        # ==================================================
        # MB/s 속도 계산
        # ==================================================

        # 측정 시간이 0이 되는 상황을 방지
        if elapsed_time > 0:

            # Byte -> MB 변환 후
            # 실제 경과 시간으로 나눠 MB/s 계산
            read_speed = (
                read_difference
                / (1024 ** 2)
                / elapsed_time
            )

            write_speed = (
                write_difference
                / (1024 ** 2)
                / elapsed_time
            )

        else:

            read_speed = 0

            write_speed = 0


        # ==================================================
        # Read / Write 속도 화면 표시
        # ==================================================

        self.read_speed_label.configure(
            text=f"{read_speed:.2f} MB/s"
        )

        self.write_speed_label.configure(
            text=f"{write_speed:.2f} MB/s"
        )


        # ==================================================
        # 다음 계산을 위해 현재 값을 이전 값으로 저장
        # ==================================================

        self.previous_read_bytes = disk["read_bytes"]

        self.previous_write_bytes = disk["write_bytes"]

        self.previous_time = current_time


        # ==================================================
        # 그래프 데이터 저장
        # ==================================================

        # 현재 시간 번호 추가
        self.time_data.append(
            self.counter
        )

        # 현재 Read 속도 추가
        self.read_data.append(
            read_speed
        )

        # 현재 Write 속도 추가
        self.write_data.append(
            write_speed
        )

        # 시간 카운터 증가
        self.counter += 1


        # ==================================================
        # 그래프 데이터 개수 제한
        # ==================================================

        # 저장된 데이터 개수가 Settings에서 설정한
        # GRAPH_HISTORY 값을 초과하면
        # 가장 오래된 데이터를 삭제
        if len(self.time_data) > config.GRAPH_HISTORY:

            # 가장 오래된 시간 데이터 삭제
            self.time_data.pop(0)

            # 가장 오래된 Read 속도 삭제
            self.read_data.pop(0)

            # 가장 오래된 Write 속도 삭제
            self.write_data.pop(0)


        # ==================================================
        # 기존 그래프 초기화
        # ==================================================

        self.ax.clear()


        # ==================================================
        # 그래프 설정 다시 적용
        # ==================================================

        self.ax.set_title(
            "Disk Read / Write Speed"
        )

        self.ax.set_ylabel(
            "MB/s"
        )

        self.ax.set_xlabel(
            "Time"
        )

        self.ax.grid(
            True
        )


        # ==================================================
        # Read Speed 그래프
        # ==================================================

        self.ax.plot(
            self.time_data,
            self.read_data,
            label="Read",
            linewidth=2
        )


        # ==================================================
        # Write Speed 그래프
        # ==================================================

        self.ax.plot(
            self.time_data,
            self.write_data,
            label="Write",
            linewidth=2
        )


        # 범례 표시
        self.ax.legend()


        # ==================================================
        # 그래프 화면 갱신
        # ==================================================

        self.canvas.draw()


        # ==================================================
        # 설정된 시간 후 다시 실행
        # ==================================================

        # Settings 페이지에서 설정한
        # UPDATE_INTERVAL 값을 그대로 사용
        #
        # 예:
        # 500  -> 0.5초
        # 1000 -> 1초
        # 2000 -> 2초
        self.after(
            config.UPDATE_INTERVAL,
            self.update_disk_info
        )
        
        