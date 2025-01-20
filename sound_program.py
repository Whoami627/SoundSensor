import RPi.GPIO as GPIO
import time
from ftplib import FTP
from datetime import datetime

# Настройка пина для цифрового сигнала с датчика звука
SOUND_PIN = 17  # GPIO пин для DO датчика

# Настройка GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SOUND_PIN, GPIO.IN)

# Настройки FTP
FTP_HOST = "hidden"  # Адрес FTP-сервера
FTP_USER = "hidden"       # Имя пользователя FTP
FTP_PASS = "hidden"       # Пароль FTP
FTP_DIR = "/test.txt"      # Директория на FTP-сервере для загрузки

# Функция для отправки файла на FTP
def upload_file(filename):
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd(FTP_DIR)

        # Открываем файл и отправляем
        with open(filename, "rb") as file:
            ftp.storbinary(f"STOR {filename}", file)

        ftp.quit()
        print(f"Файл {filename} успешно загружен на FTP-сервер.")

    except Exception as e:
        print(f"Ошибка при отправке файла на FTP: {e}")

# Основной цикл программы
try:
    while True:
        if GPIO.input(SOUND_PIN) == GPIO.HIGH:  # Если сигнал с датчика звука высокий
            print("Звук обнаружен! Генерация файла...")

            # Генерация имени файла с меткой времени
            filename = f"sound_detected_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

            # Генерация файла
            with open(filename, "w") as f:
                f.write(f"Звук был обнаружен в {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            # Отправка файла на FTP
            upload_file(filename)

            # Пауза перед следующим считыванием
            time.sleep(5)  # Пауза для предотвращения слишком частых срабатываний

        time.sleep(0.1)  # Короткая пауза для уменьшения нагрузки на процессор

except KeyboardInterrupt:
    print("Программа завершена")
    GPIO.cleanup()
