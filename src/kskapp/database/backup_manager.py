from pathlib import Path
import sys

# Это должно быть САМЫМ первым (до всех остальных импортов)
BASE_DIR = Path(__file__).resolve().parents[2]   # два уровня вверх → корень проекта
sys.path.insert(0, str(BASE_DIR))
import sqlite3
import zipfile
import os
from datetime import datetime
from PyQt5.QtWidgets import QFileDialog, QMessageBox

def backup_database_sqlite(db_path, output_path):
    """
    Создаёт резервную копию SQLite в ZIP-архиве
    """
    if not os.path.exists(db_path):
        QMessageBox.critical(None, "Ошибка", "Файл базы данных не найден.")
        return

    with zipfile.ZipFile(output_path, 'w') as zipf:
        zipf.write(db_path, os.path.basename(db_path))

    QMessageBox.information(None, "Успешно", f"Резервная копия сохранена: {output_path}")

def backup_database_mysql(output_path):
    """
    Для MySQL — нужно вызвать mysqldump (требует внешнюю утилиту)
    """
    import subprocess
    import os
    from config.database_config import DATABASE_URL

    # Пример: mysqldump -u user -p password db_name > backup.sql
    # Это требует установки MySQL CLI tools
    try:
        db_url = DATABASE_URL.replace("mysql+pymysql://", "")
        user_pass, host_db = db_url.split("@")
        user, password = user_pass.split(":")
        host, db_name = host_db.split("/", 1)

        cmd = [
            "mysqldump",
            f"--host={host}",
            f"--user={user}",
            f"--password={password}",
            db_name
        ]
        with open(output_path, 'w') as f:
            subprocess.run(cmd, stdout=f)
        QMessageBox.information(None, "Успешно", f"Резервная копия MySQL сохранена: {output_path}")
    except Exception as e:
        QMessageBox.critical(None, "Ошибка", f"Не удалось создать резервную копию MySQL: {e}")

def backup_database(output_path):
    from config.database_config import USE_SQLITE
    if USE_SQLITE:
        backup_database_sqlite("app_data.db", output_path)
    else:
        backup_database_mysql(output_path)