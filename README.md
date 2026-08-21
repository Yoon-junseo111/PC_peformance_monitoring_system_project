# PC Monitor

Python으로 개발 중인 **실시간 PC 성능 모니터링 데스크톱 애플리케이션**입니다.

CPU, NVIDIA GPU, RAM의 상태를 실시간으로 확인할 수 있으며,
`CustomTkinter`를 사용하여 Dashboard와 각 하드웨어별 상세 모니터링 페이지를 구현했습니다.

또한 Settings 페이지를 통해 프로그램의 테마와 모니터링 설정을 변경할 수 있습니다.

>  현재 개발 중인 프로젝트입니다.

---

## Features

### Dashboard

PC의 주요 하드웨어 상태를 한눈에 확인할 수 있는 메인 화면입니다.

* CPU 사용률
* GPU 사용률
* RAM 사용률
* 실시간 Progress Bar
* 하드웨어 상태 실시간 업데이트

---

### CPU Monitoring

CPU의 상세 정보를 실시간으로 확인할 수 있습니다.

* CPU 이름
* CPU 사용률
* 물리 코어 수
* 논리 코어 수
* CPU 사용률 Progress Bar
* 실시간 CPU 사용률 그래프

---

### GPU Monitoring

NVIDIA GPU의 상태를 실시간으로 확인할 수 있습니다.

* GPU 이름
* GPU 사용률
* GPU 온도
* VRAM 사용량
* 전체 VRAM 용량
* GPU 사용률 Progress Bar
* VRAM Progress Bar
* 실시간 GPU 사용률 그래프

GPU 정보는 NVIDIA NVML을 이용하여 가져옵니다.

---

### RAM Monitoring

시스템 메모리 상태를 실시간으로 확인할 수 있습니다.

* RAM 사용률
* 사용 중인 RAM
* 사용 가능한 RAM
* 전체 RAM 용량
* RAM 사용률 Progress Bar
* 실시간 RAM 사용률 그래프

---

### Settings

프로그램의 동작과 화면 설정을 변경할 수 있습니다.

#### Appearance

프로그램의 화면 테마를 변경할 수 있습니다.

* Dark
* Light
* System

#### Update Interval

CPU, GPU, RAM 정보를 가져오는 주기를 변경할 수 있습니다.

* 0.5 second
* 1 second
* 2 seconds

#### Graph History

실시간 그래프에 유지할 데이터 범위를 변경할 수 있습니다.

* 30
* 60
* 120

설정값은 `config.py`에서 관리하며 각 모니터링 페이지에서 공통으로 사용합니다.

---

## 🛠️ Tech Stack

* Python
* CustomTkinter
* psutil
* NVIDIA NVML (`nvidia-ml-py`)
* Matplotlib
* Tkinter

---

## Project Structure

```text
pc_performance_monitor_program/
│
├── main.py
├── monitor.py
├── config.py
├── requirements.txt
├── README.md
│
├── ui/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── cpu_page.py
│   ├── gpu_page.py
│   ├── ram_page.py
│   └── settings.py
│
└── assets/
    └── screenshots/
```

### `main.py`

프로그램의 메인 실행 파일입니다.

* CustomTkinter Window 생성
* Sidebar 생성
* 페이지 관리
* Dashboard / CPU / GPU / RAM / Settings 페이지 이동

### `monitor.py`

PC의 하드웨어 정보를 수집하는 역할을 담당합니다.

UI 코드와 하드웨어 모니터링 코드를 분리하기 위해 별도의 파일로 관리합니다.

현재 다음 정보를 수집합니다.

* CPU 사용률
* CPU 이름
* CPU 물리 코어
* CPU 논리 코어
* RAM 사용량
* RAM 사용률
* NVIDIA GPU 사용률
* GPU 온도
* VRAM 사용량

### `config.py`

프로그램 전체에서 공통으로 사용하는 설정값을 관리합니다.

현재 다음 설정을 관리합니다.

```python
UPDATE_INTERVAL = 1000
GRAPH_HISTORY = 30
```

`UPDATE_INTERVAL`은 하드웨어 정보 업데이트 주기를 관리하고,
`GRAPH_HISTORY`는 실시간 그래프에 유지할 데이터 개수를 관리합니다.

### `ui/`

각 페이지의 UI를 관리합니다.

* `dashboard.py` - 전체 시스템 Dashboard
* `cpu_page.py` - CPU 상세 모니터링
* `gpu_page.py` - GPU 상세 모니터링
* `ram_page.py` - RAM 상세 모니터링
* `settings.py` - 프로그램 설정

---

## Requirements

프로젝트에서 사용하는 주요 Python 라이브러리는 다음과 같습니다.

```text
customtkinter
psutil
nvidia-ml-py
matplotlib
```

필요한 라이브러리는 `requirements.txt`를 이용하여 한 번에 설치할 수 있습니다.

```bash
pip install -r requirements.txt
```

---

## Run

프로젝트를 다운로드한 후 프로젝트 폴더로 이동합니다.

```bash
cd pc_performance_monitor_program
```

필요한 라이브러리를 설치합니다.

```bash
pip install -r requirements.txt
```

프로그램을 실행합니다.

```bash
python main.py
```

---

## Screenshots

현재 개발 중인 PC Monitor의 실행 화면입니다.

<!--
이미지가 assets/screenshots/dashboard.png에 있다면
아래 주석을 제거해서 사용할 수 있습니다.

![Dashboard](assets/screenshots/dashboard.png)
-->

---

## Planned Features

앞으로 다음 기능들을 추가할 예정입니다.

* Disk 사용량 모니터링
* Disk 읽기 / 쓰기 속도
* Network 다운로드 속도
* Network 업로드 속도
* 프로세스별 CPU / RAM 사용량
* Dashboard UI 개선
* 그래프 기능 개선
* 설정값 저장
* 다중 GPU 지원
* 시스템 정보 표시
* Windows 실행 파일 (`.exe`) 패키징

---

## Development Status

**Development in Progress**

현재 구현된 기능:

* Dashboard
* CPU 상세 모니터링
* GPU 상세 모니터링
* RAM 상세 모니터링
* 실시간 사용률 그래프
* Dark / Light / System 테마
* 모니터링 업데이트 주기 설정
* Graph History 설정

다음 단계에서는 Disk 및 Network 모니터링 기능을 추가하고 전체 UI를 개선할 예정입니다.

### Disk Monitoring

- Disk 전체 용량 확인
- Disk 사용량 및 여유 공간 확인
- Disk 사용률 실시간 모니터링
- Disk Read / Write 데이터 모니터링
- Disk 상태 실시간 그래프 제공


### Network Monitoring

- 실시간 Download 속도 모니터링
- 실시간 Upload 속도 모니터링
- 누적 수신 데이터 확인
- 누적 송신 데이터 확인
- Download / Upload 실시간 그래프 제공


Dashboard에서 주요 시스템 상태를 한눈에 확인할 수 있습니다.

- CPU 사용률
- GPU 사용률
- RAM 사용률
- Disk 사용률
- Network Download / Upload 속도

## Result_screenshot

### Dashboard_result

![Dashboard_page](result/dashboard2.png)

### CPU_result

![CPU_page](result/cpu.png)

### GPU_result

![GPU_page](result/gpu.png)

### RAM_result

![RAM_page](result/ram.png)

### Settings_result

![settings_page](result/settings.png)

### Disk_result

![Disk_page](result/disk.png)

### Network_result

![Network_page](result/network.png)
