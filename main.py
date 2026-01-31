import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QStatusBar, QVBoxLayout, \
    QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor
from board_container import BoardContainer
from board_widget import CELLS_COUNT
from config import TITLE_COLOR, PLAYER_X_COLOR, PLAYER_O_COLOR, SCORE_BUTTON_ACTIVE_STYLE_SHEET, SCORE_BUTTON_INACTIVE_STYLE_SHEET, PLAY_BUTTON_ACTIVE_STYLE_SHEET, PLAY_BUTTON_INACTIVE_STYLE_SHEET

# Fonts
TITLE_FONT = QFont("Consolas", 60, QFont.Weight.Bold)
SCORE_TITLE_FONT = QFont("Consolas", 25)
TEXT_FONT = QFont("Consolas", 15)
RESTART_BUTTON_FONT = QFont("Consolas", 17)
PLAY_BUTTON_FONT = QFont("Consolas", 20)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.is_play_button_active = False

        self.initialize_ui()

        with open("styles.css", "r") as file:
            styles = file.read()
        self.setStyleSheet(styles)


    def initialize_ui(self):
        self.setGeometry(100,50,700,552)
        self.setMinimumWidth(700)
        self.setWindowTitle("Tic Tac Toe Game")
        self.generate_window()
        self.show()


    def generate_window(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30,20,50,20)
        main_widget.setLayout(main_layout)

        title = QLabel("Tic Tac Toe")
        title.setFont(TITLE_FONT)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {TITLE_COLOR}")

        content_layout = QHBoxLayout()

        main_layout.addStretch(1)
        main_layout.addWidget(title)
        main_layout.addStretch(1)
        main_layout.addLayout(content_layout, stretch=20)
        main_layout.addStretch(2)

        self.board_container = BoardContainer()
        self.board = self.board_container.board
        self.board.setObjectName("board")
        self.board.game_event.connect(self.handle_game_event)

        side_panel = self.generate_panel()

        content_layout.addStretch(1)
        content_layout.addWidget(self.board_container, stretch=5)
        content_layout.addSpacing(20)
        content_layout.addWidget(side_panel)
        content_layout.addStretch(1)


    def generate_panel(self):
        # WIDGETS
        side_panel = QWidget()
        side_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        side_panel.setMaximumWidth(300)

        score_label = QLabel("SCORE")
        score_label.setFont(SCORE_TITLE_FONT)
        score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        player_x_label = QLabel(" Player X:")
        player_x_label.setFont(TEXT_FONT)
        player_x_label.setStyleSheet(f"color: {PLAYER_X_COLOR}")
        self.player_x_score = QLabel("0 ")
        self.player_x_score.setFont(TEXT_FONT)
        self.player_x_score.setStyleSheet(f"color: {PLAYER_X_COLOR}")
        self.player_x_score.setAlignment(Qt.AlignmentFlag.AlignRight)

        player_o_label = QLabel(" Player O:")
        player_o_label.setFont(TEXT_FONT)
        player_o_label.setStyleSheet(f"color: {PLAYER_O_COLOR}")
        self.player_o_score = QLabel("0 ")
        self.player_o_score.setFont(TEXT_FONT)
        self.player_o_score.setStyleSheet(f"color: {PLAYER_O_COLOR}")
        self.player_o_score.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.restart_score_button = QPushButton("Restart Score")
        self.restart_score_button.setFont(RESTART_BUTTON_FONT)
        self.restart_score_button.setStyleSheet(SCORE_BUTTON_INACTIVE_STYLE_SHEET)
        self.restart_score_button.clicked.connect(self.restart_score)
        self.restart_score_button.setObjectName("restart_score_button")

        score_container = QWidget()
        score_container.setObjectName("score_container")
        score_container.setContentsMargins(10, 10, 10, 10)

        self.info_label = QLabel(f"Player {self.board.turn} starts!")
        self.info_label.setFont(TEXT_FONT)
        self.info_label.setStyleSheet(f"color: {PLAYER_X_COLOR if self.board.turn == 'X' else PLAYER_O_COLOR}")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.play_again_button = QPushButton("PLAY AGAIN")
        self.play_again_button.setFont(PLAY_BUTTON_FONT)
        self.play_again_button.setStyleSheet(PLAY_BUTTON_INACTIVE_STYLE_SHEET)
        self.play_again_button.clicked.connect(self.play_again)
        self.play_again_button.setObjectName("play_button")


        # LAYOUTS
        side_panel_layout = QVBoxLayout()
        side_panel_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        side_panel.setLayout(side_panel_layout)

        player_x_row = QHBoxLayout()
        player_x_row.addWidget(player_x_label)
        player_x_row.addWidget(self.player_x_score)

        player_o_row = QHBoxLayout()
        player_o_row.addWidget(player_o_label)
        player_o_row.addWidget(self.player_o_score)

        score_container_layout = QVBoxLayout()
        score_container_layout.addWidget(score_label)
        score_container_layout.addLayout(player_x_row)
        score_container_layout.addLayout(player_o_row)
        score_container_layout.addWidget(self.restart_score_button)
        score_container_layout.setSpacing(15)
        score_container.setLayout(score_container_layout)

        side_panel_layout.addWidget(score_container)
        side_panel_layout.addStretch(1)
        side_panel_layout.addWidget(self.info_label)
        side_panel_layout.addStretch(1)
        side_panel_layout.addWidget(self.play_again_button)
        side_panel_layout.addStretch(5)
        side_panel_layout.setSpacing(40)

        return side_panel


    def handle_game_event(self, event):
        self.activate_play_button(True)
        self.update_info_label(event)


    def update_info_label(self, event):
        type_ = event["type"]
        if type_ == "turn":
            turn = event["turn"]
            self.info_label.setText(f"Turn: Player {turn}")
            self.info_label.setStyleSheet(f"color: {PLAYER_X_COLOR if turn == 'X' else PLAYER_O_COLOR}")
        elif type_ == "win":
            winner = event["winner"]
            self.info_label.setText(f"Player {winner} WINS!")
            self.activate_restart_score_button(True)
            if winner == "X":
                self.info_label.setStyleSheet(f"color: {PLAYER_X_COLOR}")
                self.player_x_score.setText(f"{str(int(self.player_x_score.text()) + 1)} ")
            else:
                self.info_label.setStyleSheet(F"color: {PLAYER_O_COLOR}")
                self.player_o_score.setText(f"{str(int(self.player_o_score.text()) + 1)} ")
        elif type_ == "tie":
            self.info_label.setText("Tie!")
            self.info_label.setStyleSheet("color: #FFFF00")


    def restart_score(self):
        if self.player_x_score.text() != "0 " or self.player_o_score.text() != "0 ":
            self.player_x_score.setText("0 ")
            self.player_o_score.setText("0 ")
            self.activate_restart_score_button(False)
            self.play_again()


    def play_again(self):
        if self.is_play_button_active:
            self.is_play_button_active = False
            self.activate_play_button(False)
            self.board.board = [[None]*CELLS_COUNT for _ in range(CELLS_COUNT)]
            self.board.starting_turn = "O" if self.board.starting_turn == "X" else "X"
            self.board.turn = self.board.starting_turn
            self.board.game_active = True
            self.board.win_line = None
            self.board.update()
            self.info_label.setText(f"Player {self.board.turn} starts!")
            self.info_label.setStyleSheet(f"color: {PLAYER_X_COLOR if self.board.turn == 'X' else PLAYER_O_COLOR}")


    def activate_restart_score_button(self, activate):
        if activate:
            self.restart_score_button.setStyleSheet(SCORE_BUTTON_ACTIVE_STYLE_SHEET)
            self.restart_score_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        else:
            self.restart_score_button.setStyleSheet(SCORE_BUTTON_INACTIVE_STYLE_SHEET)
            self.restart_score_button.setCursor(QCursor(Qt.CursorShape.ArrowCursor))


    def activate_play_button(self, activate):
        if activate:
            self.play_again_button.setStyleSheet(PLAY_BUTTON_ACTIVE_STYLE_SHEET)
            self.play_again_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.is_play_button_active = True
        else:
            self.play_again_button.setStyleSheet(PLAY_BUTTON_INACTIVE_STYLE_SHEET)
            self.play_again_button.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
            self.is_play_button_active = False


    def resizeEvent(self, event):
        ratio = self.width() / self.height()
        print(ratio)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())