# ==================================================
# 라이브러리
# ==================================================

import customtkinter as ctk
import time

# monitor.py에서 하드웨어 정보 함수 가져오기
from monitor import get_cpu_info
from monitor import get_gpu_info
from monitor import get_ram_info
from monitor import get_disk_info
from monitor import get_network_info


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
        # Disk / Network 카드 영역
        # ==================================================

        # Dashboard 두 번째 줄에
        # Disk와 Network 정보를 표시하기 위한 Frame
        system_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        system_frame.pack(
            fill="x",
            padx=20,
            pady=(20, 0)
        )


        # Disk와 Network 카드가
        # 동일한 너비를 가지도록 설정
        system_frame.grid_columnconfigure(
            (0, 1),
            weight=1
        )


        # ==================================================
        # Disk 카드
        # ==================================================

        disk_card = ctk.CTkFrame(
            system_frame,
            corner_radius=15
        )

        disk_card.grid(
            row=0,
            column=0,
            padx=10,
            sticky="nsew"
        )


        # Disk 카드 제목
        disk_title = ctk.CTkLabel(
            disk_card,
            text="DISK",
            font=("Arial", 17, "bold")
        )

        disk_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        # Disk 사용률을 표시하는 Label
        self.disk_usage_label = ctk.CTkLabel(
            disk_card,
            text="0%",
            font=("Arial", 28, "bold")
        )

        self.disk_usage_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 10)
        )


        # Disk 사용률 Progress Bar
        self.disk_progress = ctk.CTkProgressBar(
            disk_card
        )

        self.disk_progress.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        # 프로그램 시작 시 0%
        self.disk_progress.set(0)


        # ==================================================
        # Network 카드
        # ==================================================

        network_card = ctk.CTkFrame(
            system_frame,
            corner_radius=15
        )

        network_card.grid(
            row=0,
            column=1,
            padx=10,
            sticky="nsew"
        )


        # Network 카드 제목
        network_title = ctk.CTkLabel(
            network_card,
            text="NETWORK",
            font=("Arial", 17, "bold")
        )

        network_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        # 현재 Download 속도
        self.download_label = ctk.CTkLabel(
            network_card,
            text="Download : 0.00 MB/s",
            font=("Arial", 16, "bold")
        )

        self.download_label.pack(
            anchor="w",
            padx=20,
            pady=(5, 5)
        )


        # 현재 Upload 속도
        self.upload_label = ctk.CTkLabel(
            network_card,
            text="Upload : 0.00 MB/s",
            font=("Arial", 16, "bold")
        )

        self.upload_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
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
        
        # ==================================================
        # Network 속도 계산을 위한 초기값
        # ==================================================

        # Network의 received_bytes와 sent_bytes는
        # 현재 속도가 아니라 누적된 데이터 값이므로
        # 이전 측정값과 현재 측정값의 차이를 이용해서
        # Download / Upload 속도를 계산해야 함

        network = get_network_info()

        # 이전에 받은 누적 데이터
        self.previous_received_bytes = network["received_bytes"]

        # 이전에 보낸 누적 데이터
        self.previous_sent_bytes = network["sent_bytes"]

        # 이전 측정 시간
        self.previous_network_time = time.time()
        
        # ==================================================
        # Disk 정보 업데이트
        # ==================================================

        # monitor.py에서 현재 Disk 정보 가져오기
        disk = get_disk_info()


        # Disk 사용률 숫자 표시
        self.disk_usage_label.configure(
            text=f"{disk['percent']:.1f}%"
        )


        # Progress Bar는 0 ~ 1 사이의 값을 사용하므로
        # Disk 사용률을 100으로 나누어서 전달
        self.disk_progress.set(
            disk["percent"] / 100
        )
        
        # =================================================
        # Network 정보 업데이트
        # ==================================================
            
        # 현재 Network 누적 정보 가져오기
        network = get_network_info()
    
    
        # 현재 측정 시간
        current_network_time = time.time()
    
    
        # 이전 측정과 현재 측정 사이에
        # 실제로 몇 초가 지났는지 계산
        elapsed_time = (
            current_network_time
            - self.previous_network_time
        )
    
    
        # ==================================================
        # Download / Upload 데이터 차이 계산
        # ==================================================
    
        # 현재 받은 누적 Byte에서
        # 이전에 받은 누적 Byte를 빼면
        # 해당 시간 동안 받은 데이터 양을 구할 수 있음
        received_difference = (
            network["received_bytes"]
            - self.previous_received_bytes
        )
    
    
        # 현재 보낸 누적 Byte에서
        # 이전에 보낸 누적 Byte를 빼면
        # 해당 시간 동안 보낸 데이터 양을 구할 수 있음
        sent_difference = (
            network["sent_bytes"]
            - self.previous_sent_bytes
        )
    
    
        # ==================================================
        # Network 속도 계산
        # ==================================================
    
        if elapsed_time > 0:
    
            # Byte -> MB 변환 후
            # 실제 경과 시간으로 나누어
            # Download 속도를 MB/s 단위로 계산
            download_speed = (
                received_difference
                / (1024 ** 2)
                / elapsed_time
            )
    
    
            # Upload 속도 계산
            upload_speed = (
                sent_difference
                / (1024 ** 2)
                / elapsed_time
            )
    
        else:
    
            # 0으로 나누는 상황 방지
            download_speed = 0
            upload_speed = 0
    
    
        # ==================================================
        # Network 정보 화면 표시
        # ==================================================
    
        self.download_label.configure(
            text=f"Download : {download_speed:.2f} MB/s"
        )
    
        self.upload_label.configure(
            text=f"Upload : {upload_speed:.2f} MB/s"
        )
    
    
        # ==================================================
        # 다음 속도 계산을 위해 현재 값 저장
        # ==================================================
    
        self.previous_received_bytes = (
            network["received_bytes"]
        )
    
        self.previous_sent_bytes = (
            network["sent_bytes"]
        )
    
        self.previous_network_time = (
            current_network_time
        )