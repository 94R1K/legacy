import time
import threading
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

lock = threading.Lock()
successful_requests = 0
failed_requests = 0


def main():
    global successful_requests
    global failed_requests
    url = 'https://www.wildberries.ru/catalog/0/search.aspx?search=%D0%BC%D0%B8%D0%BA%D1%81%D0%B5%D1%80%20%D1%81%D1%82%D1%80%D0%BE%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D0%B4%D0%BB%D1%8F%20%D1%80%D0%B0%D1%81%D1%82%D0%B2%D0%BE%D1%80%D0%B0'
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    current_height = driver.execute_script(
        "return Math.max( document.body.scrollHeight, "
        "document.body.offsetHeight,"
        "document.documentElement.clientHeight, "
        "document.documentElement.scrollHeight, "
        "document.documentElement.offsetHeight );")

    try:
        driver.get(url)
        time.sleep(10)
        while True:
            driver.execute_script(f"window.scrollTo(0, {current_height});")
            time.sleep(2)

            new_height = driver.execute_script(
                "return Math.max( document.body.scrollHeight, "
                "document.body.offsetHeight, document.documentElement.clientHeight, "
                "document.documentElement.scrollHeight, "
                "document.documentElement.offsetHeight );")

            if new_height == current_height:
                with lock:
                    successful_requests += 1
                    print(
                        f"#{successful_requests} Успешный запрос: {driver.title}")
                break

            current_height = new_height

    except WebDriverException as e:
        with lock:
            failed_requests += 1
            print(f"#{failed_requests} Ошибка при запросе: {e}")

    driver.quit()


if __name__ == "__main__":
    count_req = 30
    threads = []

    for _ in range(count_req):
        thread = threading.Thread(target=main)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Итоги: Успешные запросы: {successful_requests}, Ошибочные запросы: {failed_requests}")
