# ==================================================
# 라이브러리 불러오기
# ==================================================

# 일반 tkinter보다 디자인하기 편한 CustomTkinter
import customtkinter as ctk

# 각 화면(Page) 불러오기
from ui.Dashboard import DashboardPage
from ui.CPU_page import CPUPage
from ui.GPU_page import GPUPage
from ui.RAM_page import RAMPage
from ui.settings import SettingsPage
from ui.disk_page import DiskPage
from ui.network_page import NetworkPage


# ==================================================
# CustomTkinter 기본 설정
# ==================================================

# 기본 화면 모드
# "dark"  = 다크 모드
# "light" = 라이트 모드
# "system" = Windows 설정 따라가기
ctk.set_appearance_mode("dark")

# 기본 색상 테마
ctk.set_default_color_theme("blue")


# ==================================================
# 메인 프로그램 클래스
# ==================================================

class PCMonitorApp(ctk.CTk):

    def __init__(self):

        # 부모 클래스(CTk) 초기화
        super().__init__()

        # ==================================================
        # 메인 창 설정
        # ==================================================

        # 프로그램 제목
        self.title("PC Monitor")

        # 프로그램 창 크기
        self.geometry("1200x750")

        # 최소 창 크기
        self.minsize(1000, 650)


        # ==================================================
        # 전체 화면 Grid 설정
        # ==================================================

        # 0번 column = 사이드바
        # 1번 column = 메인 화면
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # 세로 방향은 화면 전체 사용
        self.grid_rowconfigure(0, weight=1)


        # ==================================================
        # 사이드바 생성
        # ==================================================

        self.sidebar = ctk.CTkFrame(
            self,
            width=200,
            corner_radius=0
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )


        # ==================================================
        # 프로그램 이름
        # ==================================================

        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="PC MONITOR",
            font=("Arial", 22, "bold")
        )

        self.logo_label.pack(
            padx=20,
            pady=(30, 40)
        )


        # ==================================================
        # Dashboard 버튼
        # ==================================================

        self.dashboard_button = ctk.CTkButton(
            self.sidebar,
            text="Dashboard",

            # 버튼 클릭 시 Dashboard 페이지 표시
            command=lambda: self.show_page("dashboard")
        )

        self.dashboard_button.pack(
            padx=20,
            pady=10,
            fill="x"
        )


        # ==================================================
        # CPU 버튼
        # ==================================================

        self.cpu_button = ctk.CTkButton(
            self.sidebar,
            text="CPU",
            command=lambda: self.show_page("cpu")
        )

        self.cpu_button.pack(
            padx=20,
            pady=10,
            fill="x"
        )


        # ==================================================
        # GPU 버튼
        # ==================================================

        self.gpu_button = ctk.CTkButton(
            self.sidebar,
            text="GPU",
            command=lambda: self.show_page("gpu")
        )

        self.gpu_button.pack(
            padx=20,
            pady=10,
            fill="x"
        )


        # ==================================================
        # RAM 버튼
        # ==================================================

        self.ram_button = ctk.CTkButton(
            self.sidebar,
            text="RAM",
            command=lambda: self.show_page("ram")
        )

        self.ram_button.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        # =================================================
        # Disk 버튼
        # ==================================================

        self.disk_button = ctk.CTkButton(
                self.sidebar,
                text="Disk",
                command=lambda: self.show_page("disk")
            )

        self.disk_button.pack(
                padx=20,
                pady=10,
                fill="x"
            )

        # ==================================================
        # Network 버튼
        # ==================================================

        self.network_button = ctk.CTkButton(
            self.sidebar,
            text="Network",
            command=lambda: self.show_page("network")
        )

        self.network_button.pack(
            padx=20,
            pady=10,
            fill="x"
)

        # ==================================================
        # Settings 버튼
        # ==================================================

        self.settings_button = ctk.CTkButton(
            self.sidebar,
            text="Settings",
            command=lambda: self.show_page("settings")
        )

        self.settings_button.pack(
            padx=20,
            pady=10,
            fill="x"
        )


        # ==================================================
        # 페이지가 표시될 영역
        # ==================================================

        self.page_container = ctk.CTkFrame(
            self,
            corner_radius=0
        )

        self.page_container.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        # 페이지가 창 크기에 맞게 늘어나도록 설정
        self.page_container.grid_rowconfigure(0, weight=1)
        self.page_container.grid_columnconfigure(0, weight=1)
        
        # ==================================================
        # 현재 활성 페이지
        # ==================================================

        self.current_page = "dashboard"
 
        # ==================================================
        # 페이지 생성
        # =================================================

        # 각 페이지 객체를 dictionary에 저장
        self.pages = {
            "dashboard": DashboardPage(self.page_container),
            "cpu": CPUPage(self.page_container),
            "gpu": GPUPage(self.page_container, self),
            "ram": RAMPage(self.page_container),
            "disk": DiskPage(self.page_container),
            "settings": SettingsPage(self.page_container),
            "network": NetworkPage(self.page_container),
        }


        # ==================================================
        # 페이지 배치
        # ==================================================

        # 모든 페이지를 같은 위치에 겹쳐서 배치
        # 필요한 페이지를 tkraise()로 맨 위에 올리는 방식
        for page in self.pages.values():

            page.grid(
                row=0,
                column=0,
                sticky="nsew"
            )


        # ==================================================
        # 프로그램 시작 화면
        # ==================================================

        # 처음 실행하면 Dashboard 표시
        self.show_page("dashboard")


    # ==================================================
    # 페이지 변경 함수
    # ==================================================

    def show_page(self, page_name):

           # 현재 활성 페이지 이름 저장
           self.current_page = page_name

           # 선택한 페이지 가져오기
           page = self.pages[page_name]

           # 선택한 페이지를 앞으로 가져오기
           page.tkraise()

# ==================================================
# 프로그램 실행
# ==================================================

if __name__ == "__main__":

    # 프로그램 객체 생성
    app = PCMonitorApp()

    # GUI 실행
    app.mainloop()
        
