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

# GPU 사용 가능 여부
gpu_available = False

try:

    # NVIDIA NVML 초기화
    nvmlInit()

    # 첫 번째 NVIDIA GPU 선택
    handle = nvmlDeviceGetHandleByIndex(0)

    # 여기까지 정상적으로 실행되면
    # GPU를 사용할 수 있다는 뜻
    gpu_available = True

except NVMLError as error:

    # NVIDIA GPU가 없거나
    # NVML 초기화에 실패한 경우
    print(
        f"NVIDIA GPU 초기화 실패: {error}"
    )

    # GPU 핸들은 사용할 수 없으므로 None
    handle = None
# ==================================================
# 마지막으로 정상 측정된 GPU 정보 저장
# ==================================================

last_gpu_usage = None
last_gpu_temperature = None


# ==================================================
# CPU 정보
# ==================================================

def get_cpu_info():

   
    try:
        # CPU 사용률
        cpu_usage = psutil.cpu_percent()

        # 논리 코어 개수
        logical_cores = psutil.cpu_count(logical=True)

        # 물리 코어 개수
        physical_cores = psutil.cpu_count(logical=False)

        # CPU 이름
        cpu_name = platform.processor()


        # CPU 정보 반환
        return {
            "name": cpu_name,
            "usage": cpu_usage,
            "logical_cores": logical_cores,
            "physical_cores": physical_cores
        }


    # CPU 정보 조회 중 오류가 발생한 경우
    except Exception as error:

        # 프로그램은 종료하지 않고
        # 터미널에 오류 내용만 출력
        print(
            f"CPU 정보를 가져오는 중 오류 발생: {error}"
        )


        # UI에서 사용할 기본값 반환
        return {
            "name": "CPU 정보 없음",
            "usage": 0,
            "logical_cores": 0,
            "physical_cores": 0
        }

# ================================================
# RAM 정보
# ==================================================

def get_ram_info():

    try:

        # 현재 RAM 정보 가져오기
        memory = psutil.virtual_memory()


        # ==================================================
        # Byte -> GB 변환
        # ==================================================

        # 전체 RAM
        total = memory.total / (1024 ** 3)

        # 현재 사용 중인 RAM
        used = memory.used / (1024 ** 3)

        # 현재 사용 가능한 RAM
        available = memory.available / (1024 ** 3)


        # ==================================================
        # RAM 정보 반환
        # ==================================================

        return {
            "usage": memory.percent,
            "total": total,
            "used": used,
            "available": available
        }


    # RAM 정보 조회 중 오류가 발생한 경우
    except Exception as error:

        # 프로그램 전체를 종료하지 않고
        # 오류 내용만 터미널에 출력
        print(
            f"RAM 정보를 가져오는 중 오류 발생: {error}"
        )


        # UI가 계속 동작할 수 있도록
        # 기본값 반환
        return {
            "usage": 0,
            "total": 0,
            "used": 0,
            "available": 0
        }


# ==================================================
# GPU 정보 가져오기
# ==================================================

def get_gpu_info():
    
    global last_gpu_usage
    global last_gpu_temperature
    # ==================================================
    # NVIDIA GPU 사용 가능 여부 확인
    # ==================================================

    # 프로그램 시작 시 NVML 초기화에 실패했거나
    # NVIDIA GPU를 찾지 못한 경우
    if not gpu_available:

        return {
            "name": "NVIDIA GPU 없음",
            "usage": 0,
            "temperature": 0,
            "vram_used": 0,
            "vram_total": 0
        }


    # ==================================================
    # GPU 이름 가져오기
    # ==================================================

    try:

        # 현재 선택된 GPU의 이름 가져오기
        gpu_name = nvmlDeviceGetName(handle)

        # 환경에 따라 bytes 형태로 반환될 수 있으므로
        # 문자열 형태로 변환
        if isinstance(gpu_name, bytes):
            gpu_name = gpu_name.decode()

    except NVMLError as error:

        # GPU 이름 조회에 실패해도
        # 프로그램 전체를 종료하지 않음
        print(
            f"GPU 이름을 가져오는 중 오류 발생: {error}"
        )

        gpu_name = "GPU 정보 없음"


    # ==================================================
    # GPU 사용률 가져오기
    # ==================================================

    try:

        # 현재 GPU 사용률 정보 가져오기
        utilization = nvmlDeviceGetUtilizationRates(handle)
        
        # 실제 GPU 사용률 저장
        gpu_usage = utilization.gpu
        
        # 실제 GPU 사용률
        last_gpu_usage = gpu_usage


    except NVMLError as error:

        # MX250처럼 특정 환경에서
        # 사용률 조회가 간헐적으로 실패할 수 있음
        #
        # 이 경우 다른 GPU 정보까지 없애지 않고
        # 사용률만 0으로 처리
        print(
            f"GPU 사용률을 가져오는 중 오류 발생: {error}"
        )

        gpu_usage = last_gpu_usage


    # ==================================================
    # GPU 온도 가져오기
    # ==================================================

    try:

        # 현재 GPU 온도 가져오기
        temperature = nvmlDeviceGetTemperature(
            handle,
            NVML_TEMPERATURE_GPU
        )
        
        # 정상 측정된 온도 저장
        last_gpu_temperature = temperature
        
    except NVMLError as error:

        # 온도 조회 실패 시
        # 온도만 0으로 설정
        print(
            f"GPU 온도를 가져오는 중 오류 발생: {error}"
        )

        temperature = last_gpu_temperature


    # ==================================================
    # VRAM 정보 가져오기
    # ==================================================

    try:

        # GPU 메모리 정보 가져오기
        memory = nvmlDeviceGetMemoryInfo(handle)


        # ==================================================
        # Byte -> GB 변환
        # ==================================================

        # 현재 사용 중인 VRAM
        vram_used = (
            memory.used
            / (1024 ** 3)
        )

        # 전체 VRAM 용량
        vram_total = (
            memory.total
            / (1024 ** 3)
        )

    except NVMLError as error:

        # VRAM 조회에 실패하더라도
        # 다른 GPU 정보는 계속 표시
        print(
            f"VRAM 정보를 가져오는 중 오류 발생: {error}"
        )

        vram_used = 0
        vram_total = 0


    # ==================================================
    # 최종 GPU 정보 반환
    # ==================================================

    return {

        # GPU 이름
        "name": gpu_name,

        # GPU 사용률
        "usage": gpu_usage,

        # GPU 온도
        "temperature": temperature,

        # 사용 중인 VRAM
        "vram_used": vram_used,

        # 전체 VRAM
        "vram_total": vram_total
    }
        
# ==================================================
# Disk 정보
# ==================================================

def get_disk_info():

    # Disk 정보를 가져오는 과정에서
    # 시스템 또는 psutil 관련 오류가 발생할 수 있으므로
    # try / except를 사용하여 프로그램 전체가 종료되지 않도록 처리
    try:

        # ==================================================
        # Disk 용량 정보 가져오기
        # ==================================================

        # Windows의 C 드라이브 사용 정보를 가져옴
        # total = 전체 용량
        # used = 사용 중인 용량
        # free = 남은 용량
        # percent = 사용률
        disk = psutil.disk_usage("C:\\")


        # ==================================================
        # Disk 읽기 / 쓰기 정보 가져오기
        # ==================================================

        # 시스템이 시작된 이후의
        # Disk Read / Write 누적 정보를 가져옴
        io = psutil.disk_io_counters()


        # ==================================================
        # Disk 정보 반환
        # ==================================================

        return {

            # 전체 Disk 용량
            # Byte -> GB 단위로 변환
            "total": disk.total / (1024 ** 3),

            # 현재 사용 중인 Disk 용량
            # Byte -> GB 단위로 변환
            "used": disk.used / (1024 ** 3),

            # 현재 사용 가능한 Disk 용량
            # Byte -> GB 단위로 변환
            "free": disk.free / (1024 ** 3),

            # 현재 Disk 사용률
            # 예: 78.2%
            "percent": disk.percent,

            # Disk에서 읽은 누적 데이터 양
            # io 정보가 없는 경우 0을 반환
            "read_bytes": io.read_bytes if io else 0,

            # Disk에 기록한 누적 데이터 양
            # io 정보가 없는 경우 0을 반환
            "write_bytes": io.write_bytes if io else 0
        }


    # ==================================================
    # Disk 정보 조회 실패 처리
    # ==================================================

    except Exception as error:

        # 오류가 발생하더라도 프로그램 전체를 종료하지 않고
        # 터미널에 오류 내용을 출력
        print(
            f"Disk 정보를 가져오는 중 오류 발생: {error}"
        )


        # ==================================================
        # 오류 발생 시 기본값 반환
        # ==================================================

        # Disk 정보를 가져오지 못했을 경우
        # UI에서 사용할 수 있도록 모든 값을 0으로 반환
        return {

            # 전체 용량
            "total": 0,

            # 사용 중인 용량
            "used": 0,

            # 남은 용량
            "free": 0,

            # Disk 사용률
            "percent": 0,

            # Disk Read 누적량
            "read_bytes": 0,

            # Disk Write 누적량
            "write_bytes": 0
        }


# ==================================================
# Network 정보
# ==================================================

def get_network_info():

    # Network 정보를 가져오는 과정에서도
    # 시스템 또는 psutil 관련 오류가 발생할 수 있으므로
    # try / except를 사용하여 프로그램 전체 종료를 방지
    try:

        # ==================================================
        # Network 누적 데이터 정보 가져오기
        # ==================================================

        # 현재 컴퓨터의 Network I/O 정보를 가져옴
        #
        # bytes_recv = 지금까지 받은 총 데이터
        # bytes_sent = 지금까지 보낸 총 데이터
        #
        # 여기에서 가져오는 값은 현재 속도가 아니라
        # 시스템 실행 이후의 "누적 Byte" 값
        network = psutil.net_io_counters()


        # ==================================================
        # Network 정보 반환
        # ==================================================

        return {

            # 지금까지 Network를 통해
            # 받은 총 데이터 양(Byte)
            "received_bytes": network.bytes_recv,

            # 지금까지 Network를 통해
            # 보낸 총 데이터 양(Byte)
            "sent_bytes": network.bytes_sent
        }


    # ==================================================
    # Network 정보 조회 실패 처리
    # ==================================================

    except Exception as error:

        # Network 정보를 가져오지 못해도
        # 프로그램 전체가 종료되지 않도록 오류 내용만 출력
        print(
            f"Network 정보를 가져오는 중 오류 발생: {error}"
        )


        # ==================================================
        # 오류 발생 시 기본값 반환
        # ==================================================

        # Network 정보를 읽지 못한 경우
        # Dashboard와 Network 페이지에서 사용할 수 있도록
        # 기본값 0을 반환
        return {

            # 받은 데이터 기본값
            "received_bytes": 0,

            # 보낸 데이터 기본값
            "sent_bytes": 0
        }