import sys
import os
import threading
import time
from bot_utils import send_message, click_to_target_chat

class SimpleCompiler:
    def __init__(self):
        self.variables = {}
        self.current_thread = None

    def execute_print(self, driver, wait, content):
        """Выполняет команду print с ожиданием завершения"""
        # Убираем кавычки если они есть
        if (content.startswith('"') and content.endswith('"')) or \
           (content.startswith("'") and content.endswith("'")):
            content = content[1:-1]
        
        # Создаем и запускаем поток для отправки сообщения
        self.current_thread = threading.Thread(
            target=send_message, 
            args=(driver, wait, content)
        )
        self.current_thread.start()
        
        # Ждем завершения потока
        self.current_thread.join()
        self.current_thread = None
    
    def execute_goto(self, driver, wait, chat_name):
        """Выполняет команду goto для перехода на чат"""
        # Убираем кавычки если они есть
        if (chat_name.startswith('"') and chat_name.endswith('"')) or \
           (chat_name.startswith("'") and chat_name.endswith("'")):
            chat_name = chat_name[1:-1]
        
        print(f"Переход на чат: {chat_name}")
        # Вызываем функцию перехода на чат
        click_to_target_chat(driver, wait, chat_name)
    
    def execute_wait(self, driver, wait, seconds):
        """Выполняет команду wait"""
        try:
            seconds = float(seconds)
            print(f"Ожидание {seconds} секунд...")
            time.sleep(seconds)
        except ValueError:
            print(f"Ошибка: '{seconds}' не является числом")
    
    def execute_repeat(self, driver, wait, count, commands_block):
        """Выполняет команду repeat с многострочным блоком"""
        # Проверяем на бесконечное повторение
        if count.lower() == 'inf':
            print(f"Начало выполнения бесконечного repeat")
            iteration = 1
            try:
                while True:
                    print(f"Повторение {iteration}")
                    # Выполняем все команды в блоке
                    for command_line in commands_block:
                        self.execute_command(driver, wait, command_line)
                    iteration += 1
            except KeyboardInterrupt:
                print(f"\nБесконечный repeat остановлен пользователем на итерации {iteration}")
        else:
            try:
                count = int(count)
                print(f"Начало выполнения repeat {count} раз")
                for i in range(count):
                    print(f"Повторение {i+1}/{count}")
                    # Выполняем все команды в блоке
                    for command_line in commands_block:
                        self.execute_command(driver, wait, command_line)
                print(f"Завершение repeat")
            except ValueError:
                print(f"Ошибка: '{count}' не является числом или 'inf'")
    
    def check_balanced_braces(self, text):
        """Проверяет сбалансированность фигурных скобок"""
        balance = 0
        for char in text:
            if char == '{':
                balance += 1
            elif char == '}':
                balance -= 1
            if balance < 0:
                return False, "Неожиданная закрывающая скобка '}'"
        return balance == 0, f"Незакрытая скобка: ожидается {balance} закрывающих скобок"
    
    def parse_repeat_block(self, lines, start_line_num, has_opening_brace_on_same_line):
        """Парсит многострочный блок repeat"""
        commands_block = []
        brace_balance = 1  # Уже нашли одну открывающую скобку
        
        print(f"Начало парсинга блока с строки {start_line_num + 1}")
        
        # Определяем, с какой строки начинать парсинг
        if has_opening_brace_on_same_line:
            # Если { на той же строке, начинаем со следующей строки
            start_index = start_line_num + 1
        else:
            # Если { на следующей строке, начинаем с неё
            start_index = start_line_num + 1
        
        # Ищем закрывающую скобку
        end_line_index = start_line_num
        for i in range(start_index, len(lines)):
            line = lines[i].strip()
            print(f"Строка {i+1}: '{line}' (баланс: {brace_balance})")
            
            # Пропускаем пустые строки и комментарии
            if not line or line.startswith('#'):
                continue
            
            # Считаем скобки в текущей строке
            open_braces = line.count('{')
            close_braces = line.count('}')
            brace_balance += open_braces - close_braces
            
            print(f"  Скобки: +{open_braces} -{close_braces} = баланс {brace_balance}")
            
            # Если баланс стал 0, значит блок закончился
            if brace_balance == 0:
                end_line_index = i
                # Не добавляем строку с закрывающей скобкой в команды
                if line != '}':
                    # Если на строке есть команда до }, добавляем её
                    cmd = line[:line.index('}')].strip()
                    if cmd:
                        commands_block.append(cmd)
                break
            
            # Добавляем команду в блок (убираем скобки из команды)
            clean_line = line.replace('{', '').replace('}', '').strip()
            if clean_line:
                commands_block.append(clean_line)
        
        if brace_balance != 0:
            return None, end_line_index, "Незакрытый блок repeat"
        
        print(f"Блок завершен на строке {end_line_index + 1}, команд: {len(commands_block)}")
        return commands_block, end_line_index, None
    
    def execute_command(self, driver, wait, line):
        """Выполняет одну команду"""
        line = line.strip()
        
        # Пропускаем пустые строки и комментарии
        if not line or line.startswith('#'):
            return
        
        # Обработка команды goto
        if line.startswith('goto '):
            chat_name = line[5:].strip()  # "goto " = 5 символов
            
            # Проверяем корректность строки в goto
            if not chat_name:
                print("Синтаксическая ошибка: отсутствует название чата")
                return
            
            # Проверяем сбалансированность кавычек
            if ((chat_name.startswith('"') and not chat_name.endswith('"')) or
                (chat_name.startswith("'") and not chat_name.endswith("'"))):
                print("Синтаксическая ошибка: незакрытая кавычка")
                return
            
            self.execute_goto(driver, wait, chat_name)
        
        # Обработка команды wait
        elif line.startswith('wait '):
            seconds = line[5:].strip()  # "wait " = 5 символов
            self.execute_wait(driver, wait, seconds)
        
        # Обработка команды print
        elif line.startswith('print '):
            content = line[6:].strip()  # "print " = 6 символов
            
            # Проверяем корректность строки в print
            if not content:
                print("Синтаксическая ошибка: отсутствует текст для вывода")
                return
            
            # Проверяем сбалансированность кавычек
            if ((content.startswith('"') and not content.endswith('"')) or
                (content.startswith("'") and not content.endswith("'"))):
                print("Синтаксическая ошибка: незакрытая кавычка")
                return
            
            self.execute_print(driver, wait, content)
        
        else:
            # Пропускаем одиночные закрывающие скобки
            if line == '}':
                return
            print(f"Ошибка: неизвестная команда: {line}")
    
    def compile_file(self, driver, wait, file_path):
        """Читает и выполняет код из файла"""
        try:
            if not os.path.exists(file_path):
                print(f"Ошибка: файл '{file_path}' не найден")
                return
            
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = [line.rstrip('\n') for line in file.readlines()]
                
                print(f"Загружено {len(lines)} строк из файла {file_path}")
                
                # Предварительная проверка сбалансированности скобок во всем файле
                full_text = '\n'.join(lines)
                is_balanced, error_msg = self.check_balanced_braces(full_text)
                if not is_balanced:
                    print(f"Ошибка в файле: {error_msg}")
                    return
                
                # Выполнение команд
                i = 0
                while i < len(lines):
                    line = lines[i].strip()
                    
                    try:
                        # Пропускаем пустые строки и комментарии
                        if not line or line.startswith('#'):
                            i += 1
                            continue
                        
                        print(f"Обработка строки {i+1}: '{line}'")
                        
                        # Обработка команды repeat
                        if line.startswith('repeat '):
                            # Извлекаем количество повторений
                            repeat_part = line[7:].strip()  # "repeat " = 7 символов
                            
                            # Проверяем, есть ли { на той же строке
                            has_opening_brace = '{' in repeat_part
                            
                            if has_opening_brace:
                                # Формат: repeat 10 {
                                count_str = repeat_part[:repeat_part.index('{')].strip()
                                print(f"Найдена команда repeat {count_str} с {{ на той же строке")
                                
                                # Парсим блок команд
                                commands_block, end_line_index, error = self.parse_repeat_block(
                                    lines, i, True
                                )
                            else:
                                # Формат: repeat 10\n{
                                count_str = repeat_part
                                print(f"Найдена команда repeat {count_str}")
                                
                                # Проверяем, что следующая строка - открывающая скобка
                                if i + 1 >= len(lines):
                                    print(f"Синтаксическая ошибка в строке {i+1}: после 'repeat' ожидается '{{'")
                                    i += 1
                                    continue
                                
                                next_line = lines[i + 1].strip()
                                print(f"Следующая строка: '{next_line}'")
                                
                                if next_line != '{':
                                    print(f"Синтаксическая ошибка в строке {i+2}: после 'repeat' ожидается '{{', получено '{next_line}'")
                                    i += 1
                                    continue
                                
                                # Парсим блок команд
                                commands_block, end_line_index, error = self.parse_repeat_block(
                                    lines, i + 1, False
                                )
                            
                            if error:
                                print(f"Синтаксическая ошибка: {error}")
                                i += 1
                                continue
                            
                            # Проверяем, что commands_block не None
                            if commands_block is None:
                                print("Синтаксическая ошибка: пустой блок команд")
                                i += 1
                                continue
                            
                            print(f"Найден блок repeat с {len(commands_block)} командами: {commands_block}")
                            
                            # Выполняем repeat
                            self.execute_repeat(driver, wait, count_str, commands_block)
                            
                            # Переходим на строку после закрывающей скобки
                            i = end_line_index + 1
                            print(f"Переход к строке {i + 1}")
                        else:
                            # Обычная команда
                            self.execute_command(driver, wait, line)
                            i += 1
                            
                    except Exception as e:
                        print(f"Ошибка выполнения в строке {i+1}: {e}")
                        import traceback
                        traceback.print_exc()
                        i += 1
                        
        except FileNotFoundError:
            print(f"Ошибка: файл '{file_path}' не найден")
        except PermissionError:
            print(f"Ошибка: нет доступа к файлу '{file_path}'")
        except UnicodeDecodeError:
            print(f"Ошибка: невозможно прочитать файл '{file_path}' (проблема с кодировкой)")
        except Exception as e:
            print(f"Неожиданная ошибка при чтении файла: {e}")
            import traceback
            traceback.print_exc()
    
    def stop_execution(self):
        """Останавливает выполнение текущей команды"""
        if self.current_thread and self.current_thread.is_alive():
            print("Остановка выполнения...")

def run_compiler(driver, wait):    
    file_path = "./script.botc"
    
    # Проверяем существование файла
    if not os.path.exists(file_path):
        print(f"Ошибка: файл '{file_path}' не найден")
        return
    
    if not file_path.endswith('.botc'):
        print("Предупреждение: рекомендуется использовать файлы с расширением .botc")

    compiler = SimpleCompiler()
    compiler.compile_file(driver, wait, file_path)