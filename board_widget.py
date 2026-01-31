from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QRectF, pyqtSignal
from config import BOARD_COLOR, GRID_COLOR, PLAYER_X_COLOR, PLAYER_O_COLOR, WIN_LINE_COLOR

CELLS_COUNT = 3
BOARD_PADDING = 15
BOARD_RADIUS = 15
MARKS_FONT = "Ink Free"

class BoardWidget(QWidget):
    game_event = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.board = [[None] * CELLS_COUNT for _ in range(CELLS_COUNT)]
        self.game_active = True
        self.starting_turn = "X"
        self.turn = self.starting_turn
        self.win_line = None


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        side = self.width()

        painter.setBrush(QColor(f"{BOARD_COLOR}"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, side, side, BOARD_RADIUS, BOARD_RADIUS)

        inner_side = side - 2*BOARD_PADDING

        self.draw_grid(painter, inner_side)
        self.draw_marks(painter, inner_side)
        self.draw_win_line(painter, inner_side)


    def draw_grid(self, painter, size):
        cell_size = size / CELLS_COUNT
        pen = QPen(QColor(GRID_COLOR))
        pen.setWidth(3)
        painter.setPen(pen)

        # vertical
        for i in range(1, CELLS_COUNT):
            x = BOARD_PADDING + i * cell_size
            painter.drawLine(int(x), BOARD_PADDING, int(x), int(BOARD_PADDING + size))

        # horizontal
        for i in range(1, CELLS_COUNT):
            y = BOARD_PADDING + i * cell_size
            painter.drawLine(BOARD_PADDING, int(y), int(BOARD_PADDING + size), int(y))


    def mousePressEvent(self, event):
        if not self.game_active:
            return

        side = self.width()
        inner_side = side - 2 * BOARD_PADDING

        # coordinates relative to the inner board
        x = event.position().x() - BOARD_PADDING
        y = event.position().y() - BOARD_PADDING

        # clamp within the inner board
        x = max(0, min(x, inner_side - 0.001))
        y = max(0, min(y, inner_side - 0.001))

        cell_size = inner_side / CELLS_COUNT
        col = int(x // cell_size)
        row = int(y // cell_size)

        if self.board[row][col] is None:
            self.board[row][col] = self.turn

            winner = self.check_winner()
            if winner:
                self.game_active = False
                if winner == "Tie":
                    self.game_event.emit({"type": "tie"})
                else:
                    self.game_event.emit({"type": "win", "winner": winner})
            else:
                self.turn = "O" if self.turn == "X" else "X"
                self.game_event.emit({"type": "turn", "turn": self.turn})

            self.update()


    def draw_marks(self, painter, size):
        cell_size = size / CELLS_COUNT
        font_size = int(cell_size * 0.7)  # adjusts font size to fit the cell
        font = painter.font()
        font.setFamily(MARKS_FONT)
        font.setPointSize(font_size)
        painter.setFont(font)

        for row in range(CELLS_COUNT):
            for col in range(CELLS_COUNT):
                value = self.board[row][col]
                if value is None:
                    continue

                x = BOARD_PADDING + col * cell_size
                y = BOARD_PADDING + row * cell_size

                color = QColor(PLAYER_X_COLOR if value == "X" else PLAYER_O_COLOR)
                painter.setPen(QPen(color))

                # draw the text centered
                rect = QRectF(x, y, cell_size, cell_size)
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, value)


    def check_winner(self):
        # Rows and columns
        for i in range(CELLS_COUNT):
            # Rows
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] is not None:
                self.win_line = ((0, i + 0.5), (3, i + 0.5))  # Horizontal
                return self.board[i][0]
            # Columns
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] is not None:
                self.win_line = ((i + 0.5, 0), (i + 0.5, 3))  # Vertical
                return self.board[0][i]

        # Diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            self.win_line = ((0, 0), (3, 3))  # \ diagonal
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            self.win_line = self.win_line = ((0, 3), (3, 0))  # / diagonal
            return self.board[0][2]

        # Tie
        if all(all(cell is not None for cell in row) for row in self.board):
            self.win_line = None
            return "Tie"

        self.win_line = None
        return None


    def draw_win_line(self, painter, size):
        if not self.win_line:
            return

        pen = QPen(QColor(WIN_LINE_COLOR))
        pen.setWidth(4)
        painter.setPen(pen)

        cell_size = size / CELLS_COUNT
        (x1, y1), (x2, y2) = self.win_line

        painter.drawLine(
            int(BOARD_PADDING + x1 * cell_size),
            int(BOARD_PADDING + y1 * cell_size),
            int(BOARD_PADDING + x2 * cell_size),
            int(BOARD_PADDING + y2 * cell_size),
        )






