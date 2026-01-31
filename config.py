# Palette
TITLE_COLOR = "#FF00FF"
BOARD_COLOR = "0A0A0A"
GRID_COLOR = "white"
PLAYER_X_COLOR = "#FF9500"
PLAYER_O_COLOR = "#00CED1"
WIN_LINE_COLOR = "#39FF14"
SCORE_BUTTON_ACTIVE_STYLE_SHEET = """
QPushButton#restart_score_button {
    color: white;
    background-color: #ff0088;
    padding: 10px;
}

QPushButton#restart_score_button:hover {
    background-color: red;
}

QPushButton#restart_score_button:pressed {
    background-color: rgb(119, 2, 2);
}
"""
SCORE_BUTTON_INACTIVE_STYLE_SHEET = """
QPushButton#restart_score_button {
    background-color: #862056;
}

QPushButton#restart_score_button:hover {
    background-color: #862056;
}

QPushButton#restart_score_button:pressed {
    background-color: #862056;
}
"""
PLAY_BUTTON_ACTIVE_STYLE_SHEET = """
QPushButton#play_button {
    background-color: yellow;
}

QPushButton#play_button:hover {
    background-color: greenyellow;
}

QPushButton#play_button:pressed {
    background-color: rgb(0, 255, 0);
}
"""
PLAY_BUTTON_INACTIVE_STYLE_SHEET = """
QPushButton#play_button {
    background-color: rgb(171, 171, 33);
}

QPushButton#play_button:hover {
    background-color: rgb(171, 171, 33);
}

QPushButton#play_button:pressed {
    background-color: rgb(171, 171, 33)
"""