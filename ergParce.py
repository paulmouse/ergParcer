import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def process_erg(ergPath, nclPath, nonvalidFolder):
    # Создаем список файлов с расширением ".erg" в указанной папке
    erg_files = [f for f in os.listdir(ergPath) if
                 os.path.isfile(os.path.join(ergPath, f)) and f.endswith('.erg')]
    # print()

    # Читаем лог файл, если он существует
    log_file = os.path.join(nclPath, 'ergparcerlog.txt')
    processed_files = set()
    if os.path.exists(log_file):
        with open(log_file, 'r') as file:
            processed_files = {line.strip() for line in file}

    # Обрабатываем каждый файл
    for erg_file in erg_files:
        if erg_file not in processed_files:
            # Читаем содержимое и имя файла
            with open(os.path.join(ergPath, erg_file), 'r', encoding='UTF-16') as file:
                content = file.read().rstrip('\n')
                # print(str(content))
                # input()
                file_name = os.path.splitext(erg_file)[0]
                # print(file_name)
                # print(file_name.isdigit())
                # input()

            # Записываем содержимое и имя в файл ".ncl"
            if file_name.isdigit():
                ncl_file_path = os.path.join(nclPath, file_name + '.ncl')
                with open(ncl_file_path, 'w', encoding='UTF-8') as file:
                    # print(content + file_name)
                    # input()
                    file.write(content + ' ' + file_name)
                # Записываем в лог файл
                with open(log_file, 'a') as file:
                    file.write(erg_file + '\n')
            else:
                ncl_file_path = os.path.join(nonvalidFolder, file_name + '.ncl')
                with open(ncl_file_path, 'w', encoding='UTF-8') as file:
                    # print(content + file_name)
                    # input()
                    file.write(content + ' ' + file_name)
                # Записываем в лог файл
                with open(log_file, 'a') as file:
                    file.write(erg_file + '\n')

sourceFolder = config.get("settings", 'sourceFolder')
destinationFolder = config.get("settings", "destinationFolder")
nonvalidFolder = config.get("settings", "nonvalidFolder")

process_erg(sourceFolder, destinationFolder,nonvalidFolder)