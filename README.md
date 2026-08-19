# PC Monitor

Python을 사용하여 제작 중인 실시간 PC 성능 모니터링 프로그램입니다.

CPU, RAM, NVIDIA GPU의 사용 정보를 실시간으로 확인할 수 있으며,
CustomTkinter를 이용하여 데스크톱 애플리케이션 형태의 UI를 구현하고 있습니다.

현재 프로젝트는 개발 중입니다.

---

## 주요 기능

### Dashboard

Dashboard에서 현재 PC의 주요 하드웨어 사용률을 확인할 수 있습니다.

- CPU 사용률
- GPU 사용률
- RAM 사용률
- 실시간 프로그레스 Bar

### CPU Page

CPU 전용 페이지를 구현하기 위한 기본 화면이 추가되어 있습니다.

현재는 CPU 상세 페이지의 UI 구조까지 구현되어 있으며,
추후 CPU 상세 정보와 실시간 그래프를 추가할 예정입니다.

---

## 사용 기술

- Python
- CustomTkinter
- psutil
- NVIDIA NVML (`nvidia-ml-py`)
- Tkinter

---

## 프로젝트 구조

```text
PC-Monitor/
│
├── main.py
├── monitor.py
│
├── ui/
│   ├── __init__.py
│   ├── dashboard.py
│   └── cpu_page.py
│
├── assets/
│   ├── icons/
│   └── images/
│
├── requirements.txt
└── README.md
```

### main.py

프로그램의 메인 실행 파일입니다.

- 메인 Window 생성
- Sidebar 생성
- Dashboard / CPU 페이지 이동 관리

### monitor.py

PC의 하드웨어 정보를 가져오는 역할을 담당합니다.

현재 다음 정보를 수집합니다.

- CPU 사용률
- CPU 코어 정보
- RAM 사용량
- RAM 사용률
- NVIDIA GPU 사용률
- GPU 온도
- VRAM 사용량

### dashboard.py

PC의 전체적인 사용 상태를 보여주는 Dashboard 화면입니다.

CPU, GPU, RAM 사용률을 카드 형태로 표시합니다.

### cpu_page.py

CPU의 상세 정보를 표시하기 위한 페이지입니다.

현재 기본 UI가 구현되어 있으며 상세 모니터링 기능을 추가할 예정입니다.

---

## 설치

필요한 라이브러리를 설치합니다.

```bash
pip install -r requirements.txt
```

또는 직접 설치할 경우:

```bash
pip install customtkinter psutil nvidia-ml-py matplotlib
```

---

## 실행

프로젝트 폴더에서 다음 명령어를 실행합니다.

```bash
python main.py
```

---

## 개발 예정 기능
- Settings 페이지
- Dark / Light Mode
- Disk 모니터링
- Network 모니터링

---

## 개발 상태

🚧 **Development in Progress**

현재 UI 및 모니터링 기능을 개발하고 있습니다.
