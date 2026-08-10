import psutil  # CPU 이름 등 시스템 정보를 가져오기 위한 모듈
import platform  # CPU, RAM 등의 하드웨어 정보를 가져오는 라이브러리

# cpu 사용률 확인
cpu_usage = psutil.cpu_percent(interval=1)

print("===== PC 성능 모니터 =====")

# CPU 이름
cpu_name = platform.processor()

# CPU 코어 개수
cpu_core = psutil.cpu_count()


# CPU 사용률
cpu_usage = psutil.cpu_percent(interval=1)

print(f"CPU 이름 : {cpu_name}")
print(f"CPU 코어 수 : {cpu_core}개")
print(f"CPU 사용률 : {cpu_usage}%")




