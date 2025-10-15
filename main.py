import os
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from params import *
from register_sistem import *
from bot_utils import *
import bot_actions

def run_all_accounts():
    """Запускает бота для всех аккаунтов по очереди в одной сессии"""
    accounts = list_accounts()
    if not accounts:
        print("[-] Аккаунты не найдены. Используйте --register для создания нового.")
        return
    
    print(f"[*] Найдено аккаунтов: {len(accounts)}")
    print("[*] Запуск для всех аккаунтов в ОДНОЙ сессии...")
    
    options = webdriver.FirefoxOptions()
    options.add_argument("--new-window")
    start = time.time()
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, WAIT_TIMEOUT)
    print(f"[*] Firefox стартовал за {round(time.time()-start, 2)} сек.")
    
    successful = 0
    failed = 0
    
    try:
        for i, account_file in enumerate(accounts):
            try:
                success = bot_actions.open_session(driver, wait, account_file, account_index=i, total_accounts=len(accounts))
                if success:
                    successful += 1
                else:
                    failed += 1
                    
            except Exception as e:
                print(f"[-] Критическая ошибка при обработке аккаунта {account_file}: {e}")
                failed += 1
            
            if i < len(accounts) - 1:
                print(f"[*] Пауза 2 секунды перед следующим аккаунтом...")
                time.sleep(2)
    
    except Exception as e:
        print(f"[-] Критическая ошибка в основной сессии: {e}")
        failed = len(accounts) - successful
    
    finally:
        print(f"[*] Завершение работы браузера после всех аккаунтов...")
        start = time.time()
        driver.quit()
        print(f"[*] Firefox завершился за {round(time.time()-start, 2)} сек.")
    
    print(f"\n{'='*50}")
    print(f"[ИТОГ] Успешно: {successful}, Неудачно: {failed}, Всего: {len(accounts)}")
    print(f"{'='*50}")

def main():
    ensure_directories()

    parser = argparse.ArgumentParser(description='Telegram Bot Automation')
    parser.add_argument('--register', action='store_true', 
                       help='Зарегистрировать новый аккаунт')
    parser.add_argument('--list', action='store_true',
                       help='Показать список всех аккаунтов')
    parser.add_argument('--all', action='store_true',
                       help='Запустить для всех аккаунтов (по умолчанию)')
    parser.add_argument('--account', type=str,
                       help='Указать конкретный аккаунт')
    
    args = parser.parse_args()
    
    if args.list:
        accounts = list_accounts()
        if accounts:
            print("[*] Доступные аккаунты:")
            for i, acc in enumerate(accounts):
                print(f"  {i+1}. {os.path.basename(acc)}")
            print(f"\nВсего: {len(accounts)} аккаунтов")
        else:
            print("[-] Аккаунты не найдены")
        return
    
    if args.register:
        register_new_account(args.account)
        return
    
    run_all_accounts()

if __name__ == "__main__":
    main()