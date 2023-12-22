import time
import math
import threading
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


def main(count_send: int):
    url = ("https://www.wildberries.ru/catalog/0/search.aspx?search=%D0%BC%D0%"
           "B5%D1%88%D0%B0%D0%BB%D0%BA%D0%B0%20%D0%B4%D0%BB%D1%8F%20%D1%80%D0%"
           "B0%D1%81%D1%82%D0%B2%D0%BE%D1%80%D0%B0")
    successful_requests = 1
    failed_requests = 1

    driver = webdriver.Chrome()

    current_height = 500

    for _ in range(count_send):
        try:
            # Загружаем страницу
            driver.get(url)
            print(f"#{successful_requests} Успешный запрос: {driver.title}")
            time.sleep(5)
            while True:
                driver.execute_script(f"window.scrollTo(0, {current_height});")
                time.sleep(0.5)

                new_height = driver.execute_script(
                    "return Math.max( document.body.scrollHeight, "
                    "document.body.offsetHeight, document.documentElement.clientHeight, "
                    "document.documentElement.scrollHeight, "
                    "document.documentElement.offsetHeight );"
                )
                new_height = math.ceil(new_height / 500) * 500
                if new_height == current_height:
                    print(f"#{successful_requests} Дошел до конца страницы: {driver.title}")
                    successful_requests += 1
                    current_height = 500
                    break
                print(new_height, current_height)
                # Обновить текущую высоту
                current_height += 500

        except WebDriverException as e:
            failed_requests += 1
            print(f"#{failed_requests} Ошибка при запросе: {e}")
    driver.quit()

    print(f"\nИтого успешных запросов: {successful_requests - 1}")
    print(f"Итого запросов с ошибкой: {failed_requests - 1}")


def start_threads(count_send: int):
    threads = []
    for _ in range(count_send):
        thread = threading.Thread(target=main, args=(3,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    start_threads(3)
