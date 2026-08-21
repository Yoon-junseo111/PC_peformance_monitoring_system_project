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


# ================================================
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
    
    try:
        
        # GPU 이름
        gpu_name = nvmlDeviceGetName(handle)

        # GPU 사용률
        utilization = nvmlDeviceGetUtilizationRates(handle)

        # VRAM 정보
        memory = nvmlDeviceGetMemoryInfo(handle)

        # GPU 온도
        temperature = nvmlDeviceGetTemperature(
            handle,
            NVML_TEMPERATURE_GPU
        )
        
        # bytes 형태라면 문자열로 변경
        if isinstance(gpu_name, bytes):
           gpu_name = gpu_name.decode()

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
        
           # ==================================================
    # NVIDIA GPU 정보를 가져오지 못했을 경우
    # ==================================================

    except NVMLError as error:

        print(
            f"GPU 정보를 가져오는 중 오류 발생: {error}"
        )

        # 프로그램 전체가 종료되지 않도록
        # 기본값을 반환
        return {
            "name": "GPU 정보 없음",
            "usage": 0,
            "temperature": 0,
            "vram_used": 0,
            "vram_total": 0
        }
    
# ==================================================
# Disk 정보 가져오기
# ==================================================

def get_disk_info():

    # ==================================================
    # C 드라이브 용량 정보 가져오기
    # ==================================================

    # psutil.disk_usage()를 사용하면
    # 지정한 드라이브의 전체 용량, 사용 중인 용량,
    # 남은 용량, 사용률을 가져올 수 있음
    #
    # Windows 기준으로 C:\ 드라이브를 확인
    disk = psutil.disk_usage("C:\\")


    # ==================================================
    # Byte -> GB 변환
    # ==================================================

    # psutil에서 가져온 용량은 Byte 단위이므로
    # 사용자가 보기 편하도록 GB 단위로 변환
    #
    # 1 GB = 1024 * 1024 * 1024 Byte

    total_gb = disk.total / (1024 ** 3)

    used_gb = disk.used / (1024 ** 3)

    free_gb = disk.free / (1024 ** 3)


    # ==================================================
    # Disk 읽기 / 쓰기 누적 정보
    # ==================================================

    # disk_io_counters()는 프로그램 실행 이후가 아니라
    # Windows가 부팅된 이후 Disk에서 읽고 쓴
    # 누적 Byte 정보를 가져옴
    #
    # 나중에 이전 값과 현재 값의 차이를 계산하면
    # 초당 Read / Write 속도를 구할 수 있음
    io = psutil.disk_io_counters()


    # =================================================
    # 결과 반환
    # ================================================

    return {

        # 전체 Disk 용량
        "total": total_gb,

        # 사용 중인 Disk 용량
        "used": used_gb,

        # 남은 Disk 용량
        "free": free_gb,

        # Disk 사용률
        "percent": disk.percent,

        # 누적 읽기 Byte
        "read_bytes": io.read_bytes,

        # 누적 쓰기 Byte
        "write_bytes": io.write_bytes
    }
    
    
    
# =================================================
# Network 정보 가져오기
# ================================================

def get_network_info():

    # ==================================================
    # 네트워크 송수신 정보 가져오기
    # ==================================================

    # psutil.net_io_counters()를 사용하면
    # 컴퓨터가 네트워크를 통해 주고받은
    # 데이터의 누적 정보를 가져올 수 있음
    #
    # 대표적으로:
    # bytes_recv = 받은 데이터의 누적 Byte
    # bytes_sent = 보낸 데이터의 누적 Byte
    network = psutil.net_io_counters()


    # ==================================================
    # 누적 다운로드 / 업로드 데이터
    # ==================================================

    # 지금 가져오는 값은 현재 다운로드/업로드 속도가 아니라
    # 시스템에서 네트워크를 통해 주고받은 누적 Byte 값임
    #
    # 따라서 Disk와 마찬가지로
    # 이전 값과 현재 값의 차이를 이용하면
    # 초당 Download / Upload 속도를 계산할 수 있음

    received_bytes = network.bytes_recv

    sent_bytes = network.bytes_sent


    # ==================================================
    # 결과 반환
    # =================================================

    return {

        # 네트워크를 통해 받은 누적 데이터
        # 나중에 Download Speed 계산에 사용
        "received_bytes": received_bytes,

        # 네트워크를 통해 보낸 누적 데이터
        # 나중에 Upload Speed 계산에 사용
        "sent_bytes": sent_bytes
    }