"""
Пакет для работы с графическим интерфейсом приложения Strod-Service Technology.

В этом пакете находятся модули для создания и управления окнами приложения.
"""

from .main_window import MainWindow

__all__ = [
    'MainWindow',
    'ObjectsWindow',
    'MaterialsWindow',
    'ReportsWindow'
]
