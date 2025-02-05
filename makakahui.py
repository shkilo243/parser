import requests
from bs4 import BeautifulSoup as BS
import time
import random

# Настраиваемые параметры
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    # Добавьте другие User-Agent строки
]
PROXIES = {
    'http': 'http://username:password@proxy_ip:proxy_port',
    'https': 'http://username:password@proxy_ip:proxy_port',
}
REQUEST_DELAY = (1, 3)  # Интервал между запросами в секундах
TIMEOUT = 10  # Тайм-аут запроса в секундах
MAX_RETRIES = 3  # Максимальное количество попыток запроса
VERIFY_SSL = True  # Проверка SSL-сертификата

def get_random_user_agent():
    """Возвращает случайный User-Agent из списка."""
    return random.choice(USER_AGENTS)

def make_request(url, headers=None, proxies=None, timeout=TIMEOUT, verify_ssl=VERIFY_SSL):
    """Выполняет HTTP-запрос с настраиваемыми параметрами."""
    headers = headers or {}
    proxies = proxies or {}
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(
                url,
                headers=headers,
                proxies=proxies,
                timeout=timeout,
                verify=verify_ssl
            )
            response.raise_for_status()  # Проверка на ошибки
            return response
        except requests.exceptions.RequestException as e:
            print(f"Попытка {attempt + 1} из {MAX_RETRIES} не удалась: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(random.uniform(*REQUEST_DELAY))  # Задержка перед повторной попыткой
            else:
                raise  # Повторно выбрасываем исключение после всех попыток

def save_result(data, filename="result.txt"):
    """Сохраняет результат в файл."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(data)

def parse_page(url):
    """Парсит страницу и извлекает данные."""
    headers = {
        "User-Agent": get_random_user_agent(),
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    try:
        response = make_request(url, headers=headers, proxies=PROXIES)
        
        # Парсинг HTML-контента
        html = BS(response.content, 'html.parser')
        
        # Извлечение метаданных
        metadata = {
            "url": url,
            "encoding": response.encoding,
            "status_code": response.status_code,
        }
        print("Метаданные:", metadata)
        
        # Пример извлечения данных из HTML
        title = html.title.string if html.title else "Нет заголовка"
        print(f"Заголовок страницы: {title}")
        
        # Пример извлечения текста страницы
        page_text = html.get_text()
        print("Текст страницы:")
        print(page_text[:500])  # Выводим первые 500 символов текста
        
        # Сохранение результата
        save_result(page_text, filename="page_content.txt")
        
    except Exception as e:
        print(f"Ошибка при обработке страницы: {e}")

if __name__ == "__main__":
    url = "https://example.com"  # Замените на нужный URL
    parse_page(url)
