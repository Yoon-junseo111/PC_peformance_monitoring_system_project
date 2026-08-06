import psutil
import platform
from pynvml import *


print("=" * 30)
print("      PC 성능 모니터")
print("=" * 30)

# ======================
# CPU 정보
# ======================

# CPU 이름
cpu_name = platform.processor()

# CPU 코어 개수
cpu_core = psutil.cpu_count()


# CPU 사용률
cpu_usage = psutil.cpu_percent(interval=1)

print("\n[CPU 정보]")
print(f"CPU 이름 : {cpu_name}") # 이름 출력
print(f"CPU 코어 수 : {cpu_core}개") # 코어수 출력
print(f"CPU 사용률 : {cpu_usage}%") # 사용률 출력

# =============================
# RAM 정보
# =============================

# 메모리 RAM의 전체 정보 가져오기
memory = psutil.virtual_memory()  

total_memory = memory.total / (1024 ** 3)   # (Byte -> GB 변환) (1024을 3으로 나누는 이유)
used_memory = memory.used / (1024 ** 3)     # (Byte -> GB 변환) 
available_memory = memory.available / (1024 ** 3)   # (Byte -> GB 변환) 


# 전체 메모리 출력
print("\n[RAM 정보]")
print(f"총 메모리 : {total_memory:.2f}GB")   # :.2f는 소수 둘째 자리 까지 출력
print(f"사용 중 : {used_memory:.2f}GB")      # 사용중인 메모리 출력
print(f"남은 메모리 : {available_memory:.2f}GB")   # 사용 가능한 메모리 출력
print(f"메모리 사용률 : {memory.percent}%")        # 메모리 사용률 출력


# =============================
# GPU 정보
# =============================
nvmlInit()

handle = nvmlDeviceGetHandleByIndex(0)

name = nvmlDeviceGetName(handle)
memory = nvmlDeviceGetMemoryInfo(handle)
util = nvmlDeviceGetUtilizationRates(handle)
temperature = nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)


print("\n[GPU 정보]")
print(f"GPU 이름 : {name}")
print(f"GPU 사용률 : {util.gpu}%")
print(f"GPU 메모리 : {memory.used / (1024**2):.0f}MB / {memory.total / (1024**2):.0f}MB")
print(f"GPU 온도 : {temperature}°C")

nvmlShutdown()

