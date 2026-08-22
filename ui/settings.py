# ==================================================
# 필요한 라이브러리 불러오기
# ==================================================

import customtkinter as ctk

# 프로그램 공용 설정값 가져오기
import config


# ==================================================
# Settings 페이지 클래스
# ==================================================

class SettingsPage(ctk.CTkFrame):

    def __init__(self, parent):

        # 부모 Frame 초기화
        super().__init__(parent)


        # ==================================================
        # 페이지 제목
        # ==================================================

        title = ctk.CTkLabel(
            self,
            text="Settings",
            font=("Arial", 30, "bold")
        )

        title.pack(
            anchor="w",
            padx=30,
            pady=(30, 10)
        )


        # ==================================================
        # 페이지 설명
        # ==================================================

        description = ctk.CTkLabel(
            self,
            text="PC Monitor 설정을 변경할 수 있습니다.",
            font=("Arial", 14)
        )

        description.pack(
            anchor="w",
            padx=30,
            pady=(0, 20)
        )


        # ==================================================
        # Appearance 설정 카드
        # ==================================================

        appearance_card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        appearance_card.pack(
            fill="x",
            padx=30,
            pady=10
        )


        # Appearance 제목
        appearance_title = ctk.CTkLabel(
            appearance_card,
            text="Appearance",
            font=("Arial", 18, "bold")
        )

        appearance_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        # 설명
        appearance_description = ctk.CTkLabel(
            appearance_card,
            text="프로그램의 화면 테마를 선택합니다.",
            font=("Arial", 13)
        )

        appearance_description.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )


        # Dark / Light / System 선택 메뉴
        self.appearance_menu = ctk.CTkOptionMenu(
            appearance_card,
            values=[
                "Dark",
                "Light",
                "System"
            ],
            command=self.change_appearance,
            width=200,
            height=35
        )

        self.appearance_menu.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )

        # 기본값
        self.appearance_menu.set("Dark")


        # ==================================================
        # Update Interval 설정 카드
        # ==================================================

        update_card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        update_card.pack(
            fill="x",
            padx=30,
            pady=10
        )


        # 제목
        update_title = ctk.CTkLabel(
            update_card,
            text="Update Interval",
            font=("Arial", 18, "bold")
        )

        update_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        # 설명
        update_description = ctk.CTkLabel(
            update_card,
            text="CPU, GPU, RAM 정보를 갱신하는 주기를 선택합니다.",
            font=("Arial", 13)
        )

        update_description.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )


        # 업데이트 주기 선택 메뉴
        self.update_menu = ctk.CTkOptionMenu(
            update_card,
            values=[
                "0.5 second",
                "1 second",
                "2 seconds"
            ],
            command=self.change_update_interval,
            width=200,
            height=35
        )

        self.update_menu.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )

        # 기본값
        self.update_menu.set("1 second")


        # ==================================================
        # Graph History 설정 카드
        # ==================================================

        graph_card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        graph_card.pack(
            fill="x",
            padx=30,
            pady=10
        )


        # 제목
        graph_title = ctk.CTkLabel(
            graph_card,
            text="Graph History",
            font=("Arial", 18, "bold")
        )

        graph_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )


        # 설명
        graph_description = ctk.CTkLabel(
            graph_card,
            text="그래프에 유지할 데이터 범위를 선택합니다.",
            font=("Arial", 13)
        )

        graph_description.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )


        # 그래프 표시 범위 선택 메뉴
        self.graph_menu = ctk.CTkOptionMenu(
            graph_card,
            values=[
                "30 seconds",
                "60 seconds",
                "120 seconds"
            ],
            command=self.change_graph_history,
            width=200,
            height=35
        )

        self.graph_menu.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )

        # 기본값
        self.graph_menu.set("30 seconds")


    # ==================================================
    # Appearance 변경 함수
    # ==================================================

    def change_appearance(self, mode):

        # Dark -> dark
        # Light -> light
        # System -> system
        ctk.set_appearance_mode(
            mode.lower()
        )


    # ==================================================
    # Update Interval 변경 함수
    # ==================================================

    def change_update_interval(self, value):

        # 0.5초
        if value == "0.5 second":
            config.UPDATE_INTERVAL = 500

        # 1초
        elif value == "1 second":
            config.UPDATE_INTERVAL = 1000
        # 2초
        elif value == "2 seconds":
            config.UPDATE_INTERVAL = 2000


    # ==================================================
    # Graph History 변경 함수
    # ==================================================

    def change_graph_history(self, value):

        # 최근 30개 데이터
        if value == "30 seconds":
            config.GRAPH_HISTORY = 30

        # 최근 60개 데이터
        elif value == "60 seconds":
            config.GRAPH_HISTORY = 60

        # 최근 120개 데이터
        elif value == "120 seconds":
            config.GRAPH_HISTORY = 120