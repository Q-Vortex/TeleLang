import json
import time
import os
import argparse
import glob
from datetime import datetime
from selenium import webdriver
from params import *

def register_new_account(account_name=None):
    """Регистрирует новый аккаунт"""
    account_file = get_account_filename(account_name)
    
    if os.path.exists(account_file):
        response = input(f"Аккаунт {account_file} уже существует. Перезаписать? (y/n): ")
        if response.lower() != 'y':
            print("[-] Регистрация отменена")
            return False
    
    options = webdriver.FirefoxOptions()
    options.add_argument("--new-window")
    driver = webdriver.Firefox(options=options)
    
    try:
        print(f"[*] Начата регистрация нового аккаунта: {account_file}")
        driver.get(WEB_TELEGRAM_URL)
        
        success = wait_for_user_login_collect_localstorage(driver, account_file)
        if success:
            print("[+] Регистрация завершена успешно!")
            return True
        else:
            print("[-] Регистрация не удалась")
            return False
            
    finally:
        driver.quit()

def ensure_directories():
    """Создает необходимые директории если они не существуют"""
    os.makedirs(ACCOUNTS_DIR, exist_ok=True)
    os.makedirs("private/data", exist_ok=True)

def get_account_filename(account_name=None):
    """Генерирует имя файла для аккаунта"""
    if account_name:
        return f"{ACCOUNTS_DIR}/{account_name}.json"
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{ACCOUNTS_DIR}/account_{timestamp}.json"

def has_auth_keys(localdata: dict) -> bool:
    """Проверка, есть ли в localStorage признаки авторизации Telegram"""
    if not localdata:
        return False
    keys = localdata.keys()
    indicators = ["user_auth", "dc1_auth_key", "dc2_auth_key", "dc3_auth_key", "dc4_auth_key", "dc5_auth_key",
                  "stel_web_auth", "auth_key", "session_id", "kz_version"]
    for ind in indicators:
        if ind in keys:
            return True
    for k in keys:
        if "auth" in k.lower() or k.lower().startswith("dc"):
            return True
    return False

def save_localstorage_to_file(driver, path):
    """Сохраняет localStorage в файл"""
    data = read_localstorage_from_browser(driver)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[+] LocalStorage сохранен в {path}")
    return data

def wait_for_user_login_collect_localstorage(driver, account_file, timeout=MAX_WAIT_FOR_LOGIN):
    """Ожидает появления признаков авторизации и сохраняет аккаунт"""
    start = time.time()
    last_len = -1
    
    print(f"[*] Ожидание авторизации... (максимум {timeout} секунд)")
    print("[*] Пожалуйста, войдите в свой аккаунт Telegram в открывшемся браузере")
    
    while time.time() - start < timeout:
        data = read_localstorage_from_browser(driver)
        if len(data) != last_len:
            last_len = len(data)
            print(f"[*] Обновление localStorage: {len(data)} записей")
            
        if has_auth_keys(data):
            save_localstorage_to_file(driver, account_file)
            print(f"[+] Аккаунт успешно сохранен: {account_file}")
            return True
            
        time.sleep(POLL_INTERVAL)
        
    print("[-] Не удалось обнаружить признаки авторизации в течение отведенного времени")
    return False

def list_accounts():
    """Возвращает список всех сохраненных аккаунтов"""
    pattern = os.path.join(ACCOUNTS_DIR, "*.json")
    return sorted(glob.glob(pattern))  # Сортируем для последовательности

def read_localstorage_from_browser(driver):
    """Возвращает объект localStorage как dict"""
    js = "return JSON.stringify(Object.fromEntries(Object.entries(window.localStorage)));"
    res = driver.execute_script(js)
    if res is None:
        return {}
    try:
        return json.loads(res)
    except Exception:
        return {}
    
def write_localstorage_to_browser(driver, data: dict):
    """Записывает пары ключ/значение в localStorage"""
    payload = json.dumps(data, ensure_ascii=False)
    js = f"""
    (function(){{
        const obj = JSON.parse({json.dumps(payload)});
        for (const k of Object.keys(obj)) {{
            localStorage.setItem(k, String(obj[k]));
        }}
        return true;
    }})();
    """
    return driver.execute_script(js)