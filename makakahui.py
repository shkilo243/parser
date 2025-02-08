import requests
from bs4 import BeautifulSoup as BS
import time
import random
import os

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

def make_request(url, method='GET', headers=None, proxies=None, data=None, timeout=TIMEOUT, verify_ssl=VERIFY_SSL):
    """Выполняет HTTP-запрос с настраиваемыми параметрами."""
    headers = headers or {}
    proxies = proxies or {}
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                proxies=proxies,
                data=data,
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

def clean_temp_data(filename="result.txt"):
    """Очищает временные данные."""
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Файл {filename} удален.")
    else:
        print(f"Файл {filename} не существует.")

def parse_page(url, session=None):
    """Парсит страницу и извлекает данные."""
    headers = {
        "User-Agent": get_random_user_agent(),
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    try:
        if session:
            response = session.get(url, headers=headers, proxies=PROXIES)
        else:
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
        
        # Поиск и фильтрация данных
        search_and_filter_data(html)
        
    except Exception as e:
        print(f"Ошибка при обработке страницы: {e}")

def search_and_filter_data(html):
    """Поиск и фильтрация данных на странице."""
    # Пример поиска всех ссылок на странице
    links = html.find_all('a')
    print(f"Найдено {len(links)} ссылок на странице.")
    
    # Пример фильтрации ссылок по ключевому слову
    keyword = "example"
    filtered_links = [link for link in links if keyword in link.get('href', '')]
print(f"Найдено {len(filtered_links)} ссылок, содержащих '{keyword}'.")

def handle_pagination(base_url, session=None):
    """Обход ограничений по URL (пагинация)."""
    page = 1
    while True:
        url = f"{base_url}?page={page}"
        print(f"Обработка страницы {page}: {url}")
        parse_page(url, session)
        
        # Пример условия выхода из цикла (например, если страница не найдена)
        if page >= 10:  # Ограничение на количество страниц
            break
        page += 1

if __name__ == "__main__":
    base_url = "https://example.com"  # Замените на нужный URL
    
    # Использование сессии для управления соединениями
    with requests.Session() as session:
        # Настройка сессии
        session.headers.update({"User-Agent": get_random_user_agent()})
        session.proxies.update(PROXIES)
        
        # Обработка пагинации
        handle_pagination(base_url, session)
    
    # Очистка временных данных
    clean_temp_data("page_content.txt")
        
        # Обработка пагинации
        handle_pagination(base_url, session)
    
    # Очистка временных данных
    clean_temp_data("page_content.txt")
