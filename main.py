import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException


def main(count_send: int):
    url = ("https://www.wildberries.ru/catalog/0/search.aspx?search=%D0%BC%D0%"
           "B5%D1%88%D0%B0%D0%BB%D0%BA%D0%B0%20%D0%B4%D0%BB%D1%8F%20%D1%80%D0%"
           "B0%D1%81%D1%82%D0%B2%D0%BE%D1%80%D0%B0")
    successful_requests = 1
    failed_requests = 1

    driver = webdriver.Chrome()

    current_height = driver.execute_script(
        "return Math.max("
        "document.body.scrollHeight,"
        "document.body.offsetHeight,"
        "document.documentElement.clientHeight,"
        "document.documentElement.scrollHeight,"
        "document.documentElement.offsetHeight );"
    )

    for _ in range(count_send):
        try:
            # Загружаем страницу
            driver.get(url)
            print(f"#{successful_requests} Успешный запрос: {driver.title}")
            time.sleep(5)
            while True:
                driver.execute_script(f"window.scrollTo(0, {current_height});")
                time.sleep(2)

                new_height = driver.execute_script(
                    "return Math.max( document.body.scrollHeight, "
                    "document.body.offsetHeight, document.documentElement.clientHeight, "
                    "document.documentElement.scrollHeight, "
                    "document.documentElement.offsetHeight );"
                )
                if new_height == current_height:
                    successful_requests += 1
                    break

                # Обновить текущую высоту
                current_height = new_height

        except WebDriverException as e:
            failed_requests += 1
            print(f"#{failed_requests} Ошибка при запросе: {e}")
    driver.quit()

    print(f"\nИтого успешных запросов: {successful_requests - 1}")
    print(f"Итого запросов с ошибкой: {failed_requests - 1}")


if __name__ == '__main__':
    main(3)
