#!/usr/bin/env python3
"""
Демонстрационный скрипт визуального установщика с графическим интерфейсом.
Имитирует процесс установки с согласиями, выбором пути и визуализацией прогресса.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import os


class InstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Установка приложения")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        self.install_path = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "App"))
        self.license_agreed = tk.BooleanVar()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Установка приложения", font=("Arial", 16))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Согласие с лицензией
        license_frame = ttk.LabelFrame(main_frame, text="Лицензионное соглашение", padding="10")
        license_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        license_text = tk.Text(license_frame, height=8, wrap=tk.WORD, state=tk.DISABLED)
        license_scroll = ttk.Scrollbar(license_frame, orient=tk.VERTICAL, command=license_text.yview)
        license_text.configure(yscrollcommand=license_scroll.set)
        
        license_content = """
        ЛИЦЕНЗИОННОЕ СОГЛАШЕНИЕ

        Данное программное обеспечение защищено законами об авторских правах.
        Устанавливая и используя это приложение, вы соглашаетесь со следующими условиями:

        1. Вы можете использовать это программное обеспечение в личных целях.
        2. Запрещено распространять это программное обеспечение без разрешения.
        3. Автор не несет ответственности за ущерб, причиненный использованием этого ПО.
        4. Все права собственности принадлежат разработчику.

        Нажимая "Согласен", вы подтверждаете, что прочитали и принимаете условия лицензии.
        """
        
        license_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        license_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Вставляем текст лицензии
        license_text.configure(state=tk.NORMAL)
        license_text.insert(tk.END, license_content)
        license_text.configure(state=tk.DISABLED)
        
        # Чекбокс согласия
        agreement_check = ttk.Checkbutton(license_frame, text="Я согласен с условиями лицензии", 
                                         variable=self.license_agreed)
        agreement_check.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        # Выбор пути установки
        path_frame = ttk.LabelFrame(main_frame, text="Путь установки", padding="10")
        path_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 10))
        
        ttk.Label(path_frame, text="Выберите папку для установки:").grid(row=0, column=0, sticky=tk.W)
        
        path_entry = ttk.Entry(path_frame, textvariable=self.install_path, width=50)
        path_entry.grid(row=1, column=0, padx=(0, 5), sticky=(tk.W, tk.E))
        
        browse_btn = ttk.Button(path_frame, text="Обзор...", command=self.browse_path)
        browse_btn.grid(row=1, column=1)
        
        # Кнопки навигации
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        self.next_btn = ttk.Button(button_frame, text="Далее", command=self.show_installation)
        self.next_btn.grid(row=0, column=1, padx=5)
        
        self.cancel_btn = ttk.Button(button_frame, text="Отмена", command=self.root.quit)
        self.cancel_btn.grid(row=0, column=0, padx=5)
        
        # Настройка растягивания
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        path_frame.columnconfigure(0, weight=1)
        
    def browse_path(self):
        """Открыть диалог выбора папки"""
        path = filedialog.askdirectory(initialdir=self.install_path.get())
        if path:
            self.install_path.set(path)
    
    def show_installation(self):
        """Проверить согласие и показать экран установки"""
        if not self.license_agreed.get():
            messagebox.showwarning("Предупреждение", "Вы должны согласиться с лицензионным соглашением")
            return
            
        # Очистить основной фрейм
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Создать новый интерфейс установки
        install_frame = ttk.Frame(self.root, padding="20")
        install_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Заголовок
        title_label = ttk.Label(install_frame, text="Установка приложения", font=("Arial", 16))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Прогресс бар
        self.progress = ttk.Progressbar(install_frame, mode='determinate', length=400)
        self.progress.grid(row=1, column=0, pady=10)
        
        # Статус установки
        self.status_label = ttk.Label(install_frame, text="Подготовка к установке...")
        self.status_label.grid(row=2, column=0, pady=10)
        
        # Лог установки
        log_frame = ttk.LabelFrame(install_frame, text="Ход установки", padding="5")
        log_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=10)
        
        self.log_text = tk.Text(log_frame, height=8, wrap=tk.WORD, state=tk.DISABLED)
        log_scroll = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scroll.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        
        # Кнопка отмены
        self.cancel_install_btn = ttk.Button(install_frame, text="Отмена", command=self.root.quit)
        self.cancel_install_btn.grid(row=4, column=0, pady=10)
        
        # Запустить установку в отдельном потоке
        threading.Thread(target=self.perform_installation, daemon=True).start()
    
    def perform_installation(self):
        """Имитация процесса установки"""
        steps = [
            ("Проверка системы", 10),
            ("Создание папки установки", 20),
            ("Копирование файлов", 40),
            ("Настройка параметров", 60),
            ("Создание ярлыков", 80),
            ("Завершение установки", 100)
        ]
        
        for step_name, progress_value in steps:
            # Обновить интерфейс в основном потоке
            self.root.after(0, self.update_installation_ui, step_name, progress_value)
            time.sleep(1)  # Имитация работы
        
        # Установка завершена
        self.root.after(0, self.installation_complete)
    
    def update_installation_ui(self, step_name, progress_value):
        """Обновить интерфейс установки"""
        self.status_label.config(text=step_name)
        self.progress['value'] = progress_value
        
        # Добавить запись в лог
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"• {step_name}\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)
    
    def installation_complete(self):
        """Показать экран завершения установки"""
        # Очистить основной фрейм
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Создать финальный интерфейс
        complete_frame = ttk.Frame(self.root, padding="20")
        complete_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Заголовок
        title_label = ttk.Label(complete_frame, text="Установка завершена!", font=("Arial", 16))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Описание
        desc_label = ttk.Label(complete_frame, text="Приложение успешно установлено на ваш компьютер.")
        desc_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Опции после установки
        options_frame = ttk.LabelFrame(complete_frame, text="Дополнительные действия", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.readme_var = tk.BooleanVar()
        readme_check = ttk.Checkbutton(options_frame, text="Открыть файл README", variable=self.readme_var)
        readme_check.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.launch_var = tk.BooleanVar(value=True)  # По умолчанию отмечено
        launch_check = ttk.Checkbutton(options_frame, text="Запустить приложение после установки", 
                                      variable=self.launch_var)
        launch_check.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Кнопки завершения
        button_frame = ttk.Frame(complete_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        finish_btn = ttk.Button(button_frame, text="Завершить", command=self.finish_installation)
        finish_btn.grid(row=0, column=1, padx=5)
        
        # Создать фиктивный README файл для демонстрации
        readme_path = os.path.join(self.install_path.get(), "README.txt")
        try:
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write("Добро пожаловать в установленное приложение!\n\n")
                f.write("Это файл README, содержащий информацию о приложении.\n")
                f.write("Здесь вы можете найти инструкции по использованию и другие полезные сведения.\n\n")
                f.write("Спасибо за установку!")
        except:
            pass  # Игнорировать ошибки при создании README
    
    def finish_installation(self):
        """Завершить установку и выполнить выбранные действия"""
        if self.readme_var.get():
            readme_path = os.path.join(self.install_path.get(), "README.txt")
            if os.path.exists(readme_path):
                # В реальном приложении здесь можно открыть README
                print(f"Открытие README: {readme_path}")
        
        if self.launch_var.get():
            # В реальном приложении здесь можно запустить установленное приложение
            print(f"Запуск приложения из: {self.install_path.get()}")
        
        # Показать сообщение и завершить
        messagebox.showinfo("Установка завершена", 
                           f"Приложение успешно установлено в:\n{self.install_path.get()}\n\n"
                           f"Выбранные действия выполнены.")
        self.root.quit()


def main():
    root = tk.Tk()
    app = InstallerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()