from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor


def light_mode():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(245, 245, 245))
    palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.black)
    palette.setColor(QPalette.Text, QColor(0, 0, 0))
    palette.setColor(QPalette.Button, QColor(245, 245, 245))
    palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(0, 102, 204))
    palette.setColor(QPalette.Highlight, QColor(51, 153, 255))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    return palette


def dark_mode():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(15, 15, 15))
    palette.setColor(QPalette.AlternateBase, QColor(30, 30, 30))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(30, 30, 30))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(117, 180, 255))
    palette.setColor(QPalette.Highlight, QColor(117, 180, 255))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    return palette


def dracula_mode():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(40, 42, 54))
    palette.setColor(QPalette.WindowText, QColor(248, 248, 242))
    palette.setColor(QPalette.Base, QColor(68, 71, 90))
    palette.setColor(QPalette.AlternateBase, QColor(40, 42, 54))
    palette.setColor(QPalette.Text, QColor(248, 248, 242))
    palette.setColor(QPalette.Button, QColor(68, 71, 90))
    palette.setColor(QPalette.ButtonText, QColor(248, 248, 242))
    palette.setColor(QPalette.Link, QColor(189, 147, 249))
    palette.setColor(QPalette.Highlight, QColor(98, 114, 164))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    return palette


def monokai_mode():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(39, 40, 34))
    palette.setColor(QPalette.WindowText, QColor(248, 248, 242))
    palette.setColor(QPalette.Base, QColor(39, 40, 34))
    palette.setColor(QPalette.AlternateBase, QColor(49, 50, 43))
    palette.setColor(QPalette.Text, QColor(248, 248, 242))
    palette.setColor(QPalette.Button, QColor(49, 50, 43))
    palette.setColor(QPalette.ButtonText, QColor(248, 248, 242))
    palette.setColor(QPalette.Link, QColor(102, 217, 239))
    palette.setColor(QPalette.Highlight, QColor(166, 226, 46))
    palette.setColor(QPalette.HighlightedText, QColor(39, 40, 34))
    return palette


def arc_dark_mode():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(45, 45, 48))
    palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
    palette.setColor(QPalette.Base, QColor(30, 30, 30))
    palette.setColor(QPalette.AlternateBase, QColor(45, 45, 48))
    palette.setColor(QPalette.Text, QColor(220, 220, 220))
    palette.setColor(QPalette.Button, QColor(35, 35, 35))
    palette.setColor(QPalette.ButtonText, QColor(220, 220, 220))
    palette.setColor(QPalette.Link, QColor(0, 122, 204))
    palette.setColor(QPalette.Highlight, QColor(0, 153, 204))
    palette.setColor(QPalette.HighlightedText, QColor(220, 220, 220))
    return palette
