import json
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from params import *
from register_sistem import *

# function for write localstorage to browser
def load_localstorage(driver, wait, account_info, account_file, bot_username):
  print(f"\n{'='*50}")
  print(f"[*] Запуск бота с аккаунтом: {account_info}")
  print(f"{'='*50}")
   
  driver.get(WEB_TELEGRAM_URL)
  time.sleep(1)
   
  with open(account_file, "r", encoding="utf-8") as f:
      data = json.load(f)
  write_localstorage_to_browser(driver, data)
   
  print("[+] LocalStorage загружен. Переходим к боту...")
  target = TARGET_CHAT_URL_TEMPLATE.format(bot_username)
   
  while len(driver.window_handles) > 1:
      driver.switch_to.window(driver.window_handles[-1])
      driver.close()
  driver.switch_to.window(driver.window_handles[0])
   
  driver.execute_script("window.open(arguments[0], '_blank');", target)
  driver.switch_to.window(driver.window_handles[-1])
   
  try:
      wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
      WebDriverWait(driver, 3).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, "div.message, div.msg, div.im_dialogs"))
      )
      print("[+] Контент найден")
      
  except Exception as e:
      print("[-] Контент не найден за 3 секунды, перезагружаем страницу...")
      driver.execute_script("location.reload();")
      try:
          wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
          WebDriverWait(driver, 10).until(
              EC.presence_of_element_located((By.CSS_SELECTOR, "div.message, div.msg, div.im_dialogs"))
          )
          print("[+] Контент найден после перезагрузки")
      except Exception as e2:
          print(f"[-] Контент не найден даже после перезагрузки: {e2}")
          return False

  print("[+] Готово — страница открыта с загруженным Local Storage.")
  return True

# function for click button with handling overlapping elements
def click_button(driver, wait, selector, timeout=10, check_visibility=True):
    """Нажимает кнопку с расширенной обработкой различных сценариев"""
    
    def wait_page_loaded(driver, timeout=10):
        """Ожидает полной загрузки страницы"""
        try:
            WebDriverWait(driver, timeout).until(
                lambda dr: dr.execute_script("return document.readyState") == "complete"
            )
            return True
        except Exception as e:
            # print(f"[*] Страница не загрузилась полностью: {e}")
            return False

    def is_element_clickable(element):
        """Проверяет, можно ли кликнуть по элементу"""
        try:
            # Проверяем видимость
            if not element.is_displayed():
                return False, "Элемент не видим"
            
            # Проверяем, что элемент включен
            if not element.is_enabled():
                return False, "Элемент отключен"
            
            # Проверяем, что элемент не перекрыт другими элементами
            rect = element.rect
            center_x = rect['x'] + rect['width'] / 2
            center_y = rect['y'] + rect['height'] / 2
            
            # Используем JavaScript чтобы проверить элемент в центре координат
            top_element = driver.execute_script(
                "return document.elementFromPoint(arguments[0], arguments[1]);",
                center_x, center_y
            )
            
            if top_element != element and not driver.execute_script(
                "return arguments[0].contains(arguments[1]);", top_element, element
            ):
                return False, f"Элемент перекрыт другим элементом: {top_element.tag_name}"
            
            return True, "Элемент готов к клику"
            
        except Exception as e:
            return False, f"Ошибка проверки кликабельности: {e}"

    try:
        # Шаг 1: Ждем загрузки страницы
        wait_page_loaded(driver, timeout)

        # Шаг 2: Ожидаем появления элемента с таймаутом
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        
        # Шаг 3: Проверяем кликабельность элемента
        clickable, message = is_element_clickable(element)
        
        if not clickable and check_visibility:
            # print(f"[*] Элемент найден но не кликабелен: {message}")
            
            # Пытаемся дождаться кликабельности с уменьшенным таймаутом
            try:
                short_wait = WebDriverWait(driver, 3)
                element = short_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                clickable = True
            except:
                pass

        # Шаг 4: Пытаемся кликнуть разными способами
        attempts = [
            ("Обычный клик", lambda: element.click()),
            ("ActionChains клик", lambda: ActionChains(driver).move_to_element(element).click().perform()),
            ("JavaScript клик", lambda: driver.execute_script("arguments[0].click();", element)),
            ("JavaScript через dispatchEvent", 
             lambda: driver.execute_script("""
                arguments[0].dispatchEvent(new MouseEvent('click', {
                    view: window,
                    bubbles: true,
                    cancelable: true
                }));
             """, element))
        ]

        for attempt_name, click_method in attempts:
            try:
                if not clickable and "JavaScript" not in attempt_name:
                    continue
                    
                # print(f"[*] Пробуем: {attempt_name}")
                click_method()
                
                # Проверяем успешность клика (можно добавить кастомную проверку)
                # print(f"[*] {attempt_name} успешен")
                return True
                
            except Exception as e:
                # print(f"[*] {attempt_name} не сработал: {e}")
                continue

        # print(f"[-] Все способы клика не сработали для {selector}")
        return False

    except Exception as e:
        # print(f"[-] Не удалось найти или нажать кнопку {selector}: {e}")
        return False

def send_message(driver, wait, message):
    # Ждем пока поле ввода сообщения станет доступным и видимым в текущем чате
    message_input = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.input-message-input[contenteditable='true']"))
    )
    
    # Фокусируемся на поле ввода
    driver.execute_script("arguments[0].focus();", message_input)
    
    # Очищаем поле ввода (если там есть текст)
    driver.execute_script("arguments[0].innerHTML = '';", message_input)
    
    # Вставляем сообщение
    message_input.send_keys(message)
    
    # Ждем немного, чтобы текст успел вставиться
    time.sleep(0.3)
    
    # Отправляем сообщение нажатием Enter
    message_input.send_keys(Keys.ENTER)


def click_to_target_chat(driver, wait, name):
    script = """
    return (async () => {{
        const container = document.querySelector('.chatlist-parts');
        container.scrollTop = 0;

        while (container.scrollTop < container.scrollHeight - container.clientHeight) {{
            const chats = document.querySelectorAll('.chatlist.virtual-chatlist a.chatlist-chat');
            
            for (const el of chats) {{
                if (el.querySelector('.peer-title').textContent.trim() === "{}") {{
                    el.scrollIntoView({{block: 'nearest'}});
                    return el.href;
                }}
            }}

            container.scrollTop += 80;
            await new Promise(resolve => setTimeout(resolve, 10));
        }}

        return false;
    }})();
    """.format(name)

    href = driver.execute_script(script)
    if href:
        print(f"[+] Found chat '{name}'")

        wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.input-message-input[contenteditable='true']"))
        )

        driver.refresh()
        driver.get(href)

        wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.input-message-input[contenteditable='true']"))
        )

    else:
        raise Exception(f"Чат '{name}' не найден")