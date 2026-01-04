"""
Пакет для работы с графическим интерфейсом приложения KSK Shop.

В этом пакете находятся модули для создания и управления окнами приложения.
"""

from .main_window import MainWindow

__all__ = [
    'MainWindow',
    'ObjectsWindow',
    'MaterialsWindow',
    'ReportsWindow'
]