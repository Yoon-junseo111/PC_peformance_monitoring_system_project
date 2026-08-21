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

# monitor.py에서 Network 정보 가져오기
from monitor import get_network_info

# 공용 설정값 가져오기
import config


# ==================================================
# Network 페이지 클래스
# ==================================================

class NetworkPage(ctk.CTkFrame):

    def __init__(self, parent):

        # 부모 Frame 초기화
        super().__init__(parent)


        # ==================================================
        # 그래프 데이터 저장 공간
        # ==================================================

        # X축 시간 데이터
        self.time_data = []

        # 다운로드 속도 데이터
        self.download_data = []

        # 업로드 속도 데이터
        self.upload_data = []

        # 시간 증가용 카운터
        self.counter = 0


        # ==================================================
        # 속도 계산을 위한 이전 값
        # ==================================================

        # 처음 네트워크 정보 가져오기
        first_network_info = get_network_info()

        # 이전 누적 수신 Byte
        self.previous_received_bytes = (
            first_network_info["received_bytes"]
        )

        # 이전 누적 송신 Byte
        self.previous_sent_bytes = (
            first_network_info["sent_bytes"]
        )

        # 이전 측정 시간
        self.previous_network_time = time.time()


        # ==================================================
        # 페이지 제목
        # ==================================================

        title = ctk.CTkLabel(
            self,
            text="Network",
            font=("Arial", 30, "bold")
        )

        title.pack(
            anchor="w",
            padx=30,
            pady=(30, 20)
        )


        # ==================================================
        # Download / Upload 속도 카드 영역
        # ==================================================

        speed_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        speed_frame.pack(
            fill="x",
            padx=20
        )

        # 두 카드 동일한 크기
        speed_frame.grid_columnconfigure(
            (0, 1),
            weight=1
        )


        # ==================================================
        # Download Speed 카드
        # ==================================================

        download_card = ctk.CTkFrame(
            speed_frame,
            corner_radius=15
        )

        download_card.grid(
            row=0,
            column=0,
            padx=10,
            sticky="nsew"
        )


        download_title = ctk.CTkLabel(
            download_card,
            text="Download Speed",
            font=("Arial", 17, "bold")
        )

        download_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        self.download_speed_label = ctk.CTkLabel(
            download_card,
            text="0.00 MB/s",
            font=("Arial", 30, "bold")
        )

        self.download_speed_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )


        # ==================================================
        # Upload Speed 카드
        # ==================================================

        upload_card = ctk.CTkFrame(
            speed_frame,
            corner_radius=15
        )

        upload_card.grid(
            row=0,
            column=1,
            padx=10,
            sticky="nsew"
        )


        upload_title = ctk.CTkLabel(
            upload_card,
            text="Upload Speed",
            font=("Arial", 17, "bold")
        )

        upload_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        self.upload_speed_label = ctk.CTkLabel(
            upload_card,
            text="0.00 MB/s",
            font=("Arial", 30, "bold")
        )

        self.upload_speed_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )


        # ==================================================
        # 누적 데이터 카드 영역
        # ==================================================

        total_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        total_frame.pack(
            fill="x",
            padx=20,
            pady=(20, 0)
        )

        # 두 카드 동일 크기
        total_frame.grid_columnconfigure(
            (0, 1),
            weight=1
        )


        # ==================================================
        # Total Received 카드
        # ==================================================

        received_card = ctk.CTkFrame(
            total_frame,
            corner_radius=15
        )

        received_card.grid(
            row=0,
            column=0,
            padx=10,
            sticky="nsew"
        )


        received_title = ctk.CTkLabel(
            received_card,
            text="Total Received",
            font=("Arial", 17, "bold")
        )

        received_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        self.total_received_label = ctk.CTkLabel(
            received_card,
            text="0.00 GB",
            font=("Arial", 26, "bold")
        )

        self.total_received_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )


        # ==================================================
        # Total Sent 카드
        # ==================================================

        sent_card = ctk.CTkFrame(
            total_frame,
            corner_radius=15
        )

        sent_card.grid(
            row=0,
            column=1,
            padx=10,
            sticky="nsew"
        )


        sent_title = ctk.CTkLabel(
            sent_card,
            text="Total Sent",
            font=("Arial", 17, "bold")
        )

        sent_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        self.total_sent_label = ctk.CTkLabel(
            sent_card,
            text="0.00 GB",
            font=("Arial", 26, "bold")
        )

        self.total_sent_label.pack(
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

        self.ax.set_title(
            "Network Download / Upload Speed"
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

        self.update_network_info()


    # ==================================================
    # Network 정보 실시간 업데이트 함수
    # ==================================================

    def update_network_info(self):

        # 현재 네트워크 정보 가져오기
        network = get_network_info()


        # ==================================================
        # 현재 시간
        # ==================================================

        current_time = time.time()

        # 이전 측정 시점과 현재 시점의 시간 차이
        elapsed_time = (
            current_time
            - self.previous_network_time
        )


        # ==================================================
        # 받은 Byte / 보낸 Byte 차이 계산
        # ==================================================

        # 현재 누적 수신량 - 이전 누적 수신량
        received_difference = (
            network["received_bytes"]
            - self.previous_received_bytes
        )

        # 현재 누적 송신량 - 이전 누적 송신량
        sent_difference = (
            network["sent_bytes"]
            - self.previous_sent_bytes
        )


        # ==================================================
        # Download / Upload 속도 계산
        # ==================================================

        if elapsed_time > 0:

            # Byte -> MB 변환
            # 실제 경과 시간으로 나누어 MB/s 계산
            download_speed = (
                received_difference
                / (1024 ** 2)
                / elapsed_time
            )

            upload_speed = (
                sent_difference
                / (1024 ** 2)
                / elapsed_time
            )

        else:

            download_speed = 0
            upload_speed = 0


        # ==================================================
        # 속도 화면 표시
        # ==================================================

        self.download_speed_label.configure(
            text=f"{download_speed:.2f} MB/s"
        )

        self.upload_speed_label.configure(
            text=f"{upload_speed:.2f} MB/s"
        )


        # ==================================================
        # 누적 데이터 GB 변환
        # ==================================================

        total_received_gb = (
            network["received_bytes"]
            / (1024 ** 3)
        )

        total_sent_gb = (
            network["sent_bytes"]
            / (1024 ** 3)
        )


        # ==================================================
        # 누적 데이터 화면 표시
        # ==================================================

        self.total_received_label.configure(
            text=f"{total_received_gb:.2f} GB"
        )

        self.total_sent_label.configure(
            text=f"{total_sent_gb:.2f} GB"
        )


        # ==================================================
        # 다음 계산을 위해 현재 값을 저장
        # ==================================================

        self.previous_received_bytes = (
            network["received_bytes"]
        )

        self.previous_sent_bytes = (
            network["sent_bytes"]
        )

        self.previous_network_time = current_time


        # ==================================================
        # 그래프 데이터 추가
        # ==================================================

        self.time_data.append(
            self.counter
        )

        self.download_data.append(
            download_speed
        )

        self.upload_data.append(
            upload_speed
        )

        self.counter += 1


        # ==================================================
        # 그래프 데이터 개수 제한
        # ==================================================

        # Settings의 GRAPH_HISTORY 값을 초과하면
        # 가장 오래된 데이터를 제거
        if len(self.time_data) > config.GRAPH_HISTORY:

            # 가장 오래된 시간 삭제
            self.time_data.pop(0)

            # 가장 오래된 Download 데이터 삭제
            self.download_data.pop(0)

            # 가장 오래된 Upload 데이터 삭제
            self.upload_data.pop(0)


        # ==================================================
        # 기존 그래프 초기화
        # ==================================================

        self.ax.clear()


        # ==================================================
        # 그래프 기본 설정 다시 적용
        # ==================================================

        self.ax.set_title(
            "Network Download / Upload Speed"
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
        # Download 그래프
        # ==================================================

        self.ax.plot(
            self.time_data,
            self.download_data,
            label="Download",
            linewidth=2
        )


        # ==================================================
        # Upload 그래프
        # ==================================================

        self.ax.plot(
            self.time_data,
            self.upload_data,
            label="Upload",
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

        self.after(
            config.UPDATE_INTERVAL,
            self.update_network_info
        )
        
      