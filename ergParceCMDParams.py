import os
import configparser
import argparse

config = configparser.ConfigParser()
config.read('config.ini')

# inputType = config.get("files", "inputType")
# outputType = config.get("files", "outputType")
inputType = '.erg'
outputType = '.ncl'
def process_erg(ergPath, nclPath, nonvalidFolder, inputType, outputType):
    # Создаем список файлов с расширением ".erg" в указанной папке
    erg_files = [f for f in os.listdir(ergPath) if
                 os.path.isfile(os.path.join(ergPath, f)) and f.endswith(inputType)]

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
                file_name = os.path.splitext(erg_file)[0]

            # Записываем содержимое и имя в файл ".ncl"
            if file_name.isdigit():
                ncl_file_path = os.path.join(nclPath, file_name + outputType)
                with open(ncl_file_path, 'w', encoding='UTF-8') as file:
                    file.write(content + ' ' + file_name)
                # Записываем в лог файл
                with open(log_file, 'a') as file:
                    file.write(erg_file + '\n')
            else:
                ncl_file_path = os.path.join(nonvalidFolder, file_name + outputType)
                with open(ncl_file_path, 'w', encoding='UTF-8') as file:
                    file.write(content + ' ' + file_name)
                # Записываем в лог файл
                with open(log_file, 'a') as file:
                    file.write(erg_file + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process .erg files and generate .ncl files.")
    parser.add_argument("--sourceFolder", type=str, help="Path to the source folder containing .erg files.")
    parser.add_argument("--destinationFolder", type=str, help="Path to the destination folder for valid .ncl files.")
    parser.add_argument("--nonvalidFolder", type=str, help="Path to the folder for non-valid .ncl files.")

    args = parser.parse_args()

    # Путь к config.ini, расположенному рядом с исполняемым файлом
    # config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')

    # Чтение значений из config.ini, если параметры не заданы
    sourceFolder = args.sourceFolder if args.sourceFolder else config.get("settings", 'sourceFolder')
    destinationFolder = args.destinationFolder if args.destinationFolder else config.get("settings", "destinationFolder")
    nonvalidFolder = args.nonvalidFolder if args.nonvalidFolder else config.get("settings", "nonvalidFolder")

    process_erg(sourceFolder, destinationFolder, nonvalidFolder, inputType, outputType)
