import os     # 화면을 지우기 위해 사용
import time   # 일정 시간 동안 대기하기 위한 모듈
import platform  # CPU 이름 등 시스템 정보를 가져오는 라이브러리
import psutil    # CPU, RAM 등의 하드웨어 정보를 가져오는 라이브러리
from pynvml import *  # NVIDIA GPU 정보를 가져오기 위한 라이브러리 

nvmlInit()


# 대부분의 PC는 GPU가 하나이므로 0번을 사용
handle = nvmlDeviceGetHandleByIndex(0)

while True:
    
    os.system("cls") # 콘솔 화면 제거
    
# ======================
# CPU 정보
# ======================

# CPU 이름 불러오기
cpu_name = platform.processor()   

# CPU 사용률 측정
# interval = 1은 1초 동안 CPU 사용률을 측정한 후 값을 반환한다.
cpu_usage = psutil.cpu_percent(interval=1)

# CPU의 논리 코어 개수를 가져오기
cpu_core = psutil.cpu_count()

# ===================
# RAM 정보
# ===================

memory = psutil.virtual_memory()

print("\n[RAM]")

# 메모리 사용률
print(f"사용률 : {memory.percent}%")

# 사용 중인 메모리 (Byte -> GB 변환) (1024을 3으로 나누는 이유)
print(f"사용중 : {memory.used / (1024 ** 3):.2f} GB")

# 사용 가능한 메모리 (Byte -> GB 변환)
print(f"남음 : {memory.available / (1024 ** 3):.2f} GB")

# ====================
# GPU 정보
# ====================


# GPU 이름 가져오기 
name = nvmlDeviceGetName(handle)

# GPU 사용률 가져오기 
util - nvmlDeviceGetUtilizationRates(handle)

# GPU 메모리 가져오기
gpu_memory = nvmlDevicegetmemoryinfo(handle)

# GPU 온도값 가져오기
temperature = nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)

print("\n[GPU]")
print(f"이름 : {name}")

# GPU 사용률 출력
print(f"사용률 : {util.gpu}%")


# GPU 온도 출력
print(f"온도 : {temperature}°C")

# GPU 메모리 사용량 출력
print(f"VRAM : {gpu_memory.used / (1024 ** 2):.0f}MB / {gpu_memory.total / (1024 ** 2):.0f}MB")

# 1초 동안 대기한 후 다시 반복
time.sleep(1)


 