import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from compiler import run_compiler
from params import *
from register_sistem import *
from bot_utils import *

def open_session(driver, wait, account_file, account_index=None, total_accounts=None, bot_username=STARSOV_BOT_USERNAME):
    """Запускает полную последовательность действий бота для указанного аккаунта в существующей сессии"""
    if not os.path.exists(account_file):
        print(f"[-] Файл аккаунта не найден: {account_file}")
        return False
    
    if account_index is not None and total_accounts is not None:
        account_info = f"[{account_index+1}/{total_accounts}] {os.path.basename(account_file)}"
    else:
        account_info = os.path.basename(account_file)
    
    try:
        if not load_localstorage(driver, wait, account_info, account_file, bot_username):
            print(f"[-] Не удалось загрузить LocalStorage для {account_info}")
            return False
        
        try:
            run_compiler(driver, wait)
            input("Press Enter to start script...")
        except Exception as e:
            print(f"[-] Ошибка при выполнении действий бота: {e}")
            return False
        
        return True
    
    except Exception as e:
        print(f"[-] Общая ошибка при работе с аккаунтом: {e}")
        return False
    finally:
        print(f"[*] Завершено для аккаунта {account_info}")