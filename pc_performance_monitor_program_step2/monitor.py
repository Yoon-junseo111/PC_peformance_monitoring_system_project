# ==================================================
# 라이브러리
# ==================================================

# CPU / RAM 정보
import psutil

# CPU 이름 등 시스템 정보
import platform

# NVIDIA GPU 정보
from pynvml import *


# ==================================================
# NVIDIA GPU 초기화
# ==================================================

# NVIDIA Management Library 시작
nvmlInit()

# 첫 번째 NVIDIA GPU 선택
handle = nvmlDeviceGetHandleByIndex(0)


# ==================================================
# CPU 정보
# ==================================================

def get_cpu_info():

    # CPU 사용률
    cpu_usage = psutil.cpu_percent()

    # 논리 코어 개수
    logical_cores = psutil.cpu_count(logical=True)

    # 물리 코어 개수
    physical_cores = psutil.cpu_count(logical=False)

    # CPU 이름
    cpu_name = platform.processor()

    # dictionary 형태로 결과 반환
    return {
        "name": cpu_name,
        "usage": cpu_usage,
        "logical_cores": logical_cores,
        "physical_cores": physical_cores
    }


# ==================================================
# RAM 정보
# ==================================================

def get_ram_info():

    # 현재 RAM 정보 가져오기
    memory = psutil.virtual_memory()

    # Byte → GB 변환
    total = memory.total / (1024 ** 3)
    used = memory.used / (1024 ** 3)
    available = memory.available / (1024 ** 3)

    return {
        "usage": memory.percent,
        "total": total,
        "used": used,
        "available": available
    }


# ==================================================
# GPU 정보
# ==================================================

def get_gpu_info():

    # GPU 이름
    gpu_name = nvmlDeviceGetName(handle)

    # bytes 형태라면 문자열로 변경
    if isinstance(gpu_name, bytes):
        gpu_name = gpu_name.decode()

    # GPU 사용률
    utilization = nvmlDeviceGetUtilizationRates(handle)

    # VRAM 정보
    memory = nvmlDeviceGetMemoryInfo(handle)

    # GPU 온도
    temperature = nvmlDeviceGetTemperature(
        handle,
        NVML_TEMPERATURE_GPU
    )

    # Byte → GB
    vram_used = memory.used / (1024 ** 3)
    vram_total = memory.total / (1024 ** 3)

    return {
        "name": gpu_name,
        "usage": utilization.gpu,
        "temperature": temperature,
        "vram_used": vram_used,
        "vram_total": vram_total
    }