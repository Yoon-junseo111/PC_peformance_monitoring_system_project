import tkinter as tk
from tkinter import ttk

import platform
import psutil

# NVIDIA GPU 정보를 가져오기 위한 라이브러리
from pynvml import *

# 그래프를 만들기 위한 라이브러리
import matplotlib.pyplot as plt

# Tkinter 안에 matplotlib 그래프를 넣기 위한 기능
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ==================================================
# Matplotlib 한글 설정
# ==================================================

# Windows 기본 한글 폰트 사용
plt.rcParams["font.family"] = "Malgun Gothic"

# 마이너스 기호 깨짐 방지
plt.rcParams["axes.unicode_minus"] = False


# ==================================================
# NVIDIA GPU 초기화
# ==================================================

nvmlInit()

# 첫 번째 GPU 선택
handle = nvmlDeviceGetHandleByIndex(0)


# ==================================================
# GUI 창 생성
# ==================================================

window = tk.Tk()

# 프로그램 제목
window.title("PC 성능 모니터")

# 창 크기
window.geometry("850x900")

# 창 크기 변경 방지
window.resizable(False, False)


# ==================================================
# 프로그램 제목
# ==================================================

title_label = tk.Label(
    window,
    text="PC 성능 모니터",
    font=("Arial", 24, "bold")
)

title_label.pack(pady=15)


# ==================================================
# CPU
# ==================================================

cpu_label = tk.Label(
    window,
    text="CPU",
    font=("Arial", 16, "bold")
)

cpu_label.pack()


cpu_info = tk.Label(
    window,
    text="CPU 정보를 불러오는 중...",
    font=("Arial", 11)
)

cpu_info.pack(pady=3)


# CPU 사용률 Progressbar
cpu_progress = ttk.Progressbar(
    window,
    length=600,
    maximum=100
)

cpu_progress.pack(pady=5)


# ==================================================
# RAM
# ==================================================

ram_label = tk.Label(
    window,
    text="RAM",
    font=("Arial", 16, "bold")
)

ram_label.pack(pady=(10, 0))


ram_info = tk.Label(
    window,
    text="RAM 정보를 불러오는 중...",
    font=("Arial", 11)
)

ram_info.pack(pady=3)


# RAM 사용률 Progressbar
ram_progress = ttk.Progressbar(
    window,
    length=600,
    maximum=100
)

ram_progress.pack(pady=5)


# ==================================================
# GPU
# ==================================================

gpu_label = tk.Label(
    window,
    text="GPU",
    font=("Arial", 16, "bold")
)

gpu_label.pack(pady=(10, 0))


gpu_info = tk.Label(
    window,
    text="GPU 정보를 불러오는 중...",
    font=("Arial", 11)
)

gpu_info.pack(pady=3)


# GPU 사용률 Progressbar
gpu_progress = ttk.Progressbar(
    window,
    length=600,
    maximum=100
)

gpu_progress.pack(pady=5)


# ==================================================
# 그래프 데이터
# ==================================================

# 시간 데이터
time_data = []

# CPU 사용률 데이터
cpu_data = []

# RAM 사용률 데이터
ram_data = []

# GPU 사용률 데이터
gpu_data = []

# 그래프에 표시할 최대 데이터 개수
max_data = 30


# ==================================================
# 그래프 생성
# ==================================================

figure = plt.Figure(
    figsize=(7.8, 4.2),
    dpi=100
)

# 그래프 영역 생성
ax = figure.add_subplot(111)

# 그래프 제목
ax.set_title("실시간 PC 사용률")

# Y축 범위
ax.set_ylim(0, 100)

# Y축 이름
ax.set_ylabel("사용률 (%)")

# X축 이름
ax.set_xlabel("시간 (초)")

# 격자 표시
ax.grid(True)


# Tkinter에 그래프 연결
canvas = FigureCanvasTkAgg(
    figure,
    master=window
)

canvas.get_tk_widget().pack(pady=15)


# ==================================================
# 실시간 정보 업데이트 함수
# ==================================================

def update_info():

    # ==================================================
    # CPU 정보
    # ==================================================

    # CPU 이름
    cpu_name = platform.processor()

    # CPU 사용률
    cpu_usage = psutil.cpu_percent(interval=0.1)

    # CPU 논리 코어 수
    cpu_core = psutil.cpu_count()


    # CPU 정보 표시
    cpu_info.config(
        text=
        f"이름 : {cpu_name} | "
        f"코어 : {cpu_core}개 | "
        f"사용률 : {cpu_usage:.1f}%"
    )


    # CPU Progressbar 변경
    cpu_progress["value"] = cpu_usage


    # ==================================================
    # RAM 정보
    # ==================================================

    # RAM 정보 가져오기
    memory = psutil.virtual_memory()

    # Byte → GB 변환
    total_memory = memory.total / (1024 ** 3)

    used_memory = memory.used / (1024 ** 3)

    available_memory = memory.available / (1024 ** 3)


    # RAM 정보 표시
    ram_info.config(
        text=
        f"전체 : {total_memory:.2f} GB | "
        f"사용 중 : {used_memory:.2f} GB | "
        f"남음 : {available_memory:.2f} GB | "
        f"사용률 : {memory.percent:.1f}%"
    )


    # RAM Progressbar 변경
    ram_progress["value"] = memory.percent


    # ==================================================
    # GPU 정보
    # ==================================================

    # GPU 이름
    gpu_name = nvmlDeviceGetName(handle)

    # GPU 사용률
    gpu_utilization = nvmlDeviceGetUtilizationRates(handle)

    # GPU 메모리 정보
    gpu_memory = nvmlDeviceGetMemoryInfo(handle)

    # GPU 온도
    temperature = nvmlDeviceGetTemperature(
        handle,
        NVML_TEMPERATURE_GPU
    )


    # GPU 이름이 bytes 형태인 경우 문자열로 변환
    if isinstance(gpu_name, bytes):
        gpu_name = gpu_name.decode()


    # GPU 사용률
    gpu_usage = gpu_utilization.gpu


    # GPU 정보 표시
    gpu_info.config(
        text=
        f"이름 : {gpu_name} | "
        f"사용률 : {gpu_usage}% | "
        f"온도 : {temperature}°C | "
        f"VRAM : "
        f"{gpu_memory.used / (1024 ** 2):.0f} / "
        f"{gpu_memory.total / (1024 ** 2):.0f} MB"
    )


    # GPU Progressbar 변경
    gpu_progress["value"] = gpu_usage


    # ==================================================
    # 그래프 데이터 추가
    # ==================================================

    # 현재 시간
    # 0 → 1 → 2 → 3 → 4 ...
    current_time = len(time_data)


    # 각 데이터를 리스트에 추가
    time_data.append(current_time)

    cpu_data.append(cpu_usage)

    ram_data.append(memory.percent)

    gpu_data.append(gpu_usage)


    # ==================================================
    # 최근 30개 데이터만 유지
    # ==================================================

    if len(time_data) > max_data:

        time_data.pop(0)

        cpu_data.pop(0)

        ram_data.pop(0)

        gpu_data.pop(0)


    # ==================================================
    # 그래프 초기화
    # ==================================================

    ax.clear()


    # ==================================================
    # 그래프 설정
    # ==================================================

    ax.set_title("실시간 PC 사용률")

    ax.set_ylim(0, 100)

    ax.set_ylabel("사용률 (%)")

    ax.set_xlabel("시간 (초)")

    ax.grid(True)


    # ==================================================
    # CPU 선 그래프
    # ==================================================

    ax.plot(
        time_data,
        cpu_data,
        label="CPU",
        linewidth=2
    )


    # ==================================================
    # RAM 선 그래프
    # ==================================================

    ax.plot(
        time_data,
        ram_data,
        label="RAM",
        linewidth=2
    )


    # ==================================================
    # GPU 선 그래프
    # ==================================================

    ax.plot(
        time_data,
        gpu_data,
        label="GPU",
        linewidth=2
    )


    # ==================================================
    # 범례
    # ==================================================

    ax.legend()


    # ==================================================
    # 그래프 다시 그리기
    # ==================================================

    canvas.draw()


    # ==================================================
    # 1초 후 다시 실행
    # ==================================================

    window.after(1000, update_info)


# ==================================================
# 프로그램 시작
# ==================================================

update_info()

window.mainloop()


# ==================================================
# NVIDIA GPU 종료
# ==================================================

nvmlShutdown()