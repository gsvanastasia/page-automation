import json
import time
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()


@pytest.fixture(scope="module", autouse=True)
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


page_url = "https://www.avito.ru/avito-care/eco-impact"
api_url = "**/web/1/charity/ecoImpact/init"
api_response = {
    "result": {
        "blocks": {
            "personalImpact": {
                "avatarUrl": "https://static.avito.ru/stub_avatars/%D0%90/13_256x256.png",
                "data": {
                    "co2": 0,
                    "energy": 0,
                    "materials": 1,
                    "pineYears": 2,
                    "water": 0
                }
            }
        },
        "isAuthorized": True
    },
    "status": "ok"
}

def fill_response(co2, energy, water):
    api_response["result"]["blocks"]["personalImpact"]["data"]["co2"] = co2
    api_response["result"]["blocks"]["personalImpact"]["data"]["energy"] = energy
    api_response["result"]["blocks"]["personalImpact"]["data"]["water"] = water
    return api_response

def fulfill_route(route, response):
    route.fulfill(
        body=json.dumps(response),
        status=200,
        headers={"Content-Type": "application/json"}
    )

# 1. Проверка отображения значений счётчиков равных 0
def test_01(page):
    def route_handler(route):
        fulfill_route(route, fill_response(0, 0, 0))

    page.route(api_url, route_handler)

    page.goto(page_url, timeout=120000)

    page.locator('.desktop-impact-item-eeQO3').nth(1).screenshot(path="output/01_co2.png")
    page.locator('.desktop-impact-item-eeQO3').nth(3).screenshot(path="output/01_water.png")
    page.locator('.desktop-impact-item-eeQO3').nth(5).screenshot(path="output/01_energy.png")

# 2. Проверка отображения значений счётчиков после получения корректных данных от бэкенда  575
def test_02(page):
    def route_handler(route):
        fulfill_route(route, fill_response(575, 575, 575))

    page.route(api_url, route_handler)

    page.goto(page_url, timeout=120000)

    page.locator('.desktop-impact-item-eeQO3').nth(1).screenshot(path="output/02_co2.png")
    page.locator('.desktop-impact-item-eeQO3').nth(3).screenshot(path="output/02_water.png")
    page.locator('.desktop-impact-item-eeQO3').nth(5).screenshot(path="output/02_energy.png")

# 3. Проверка на корректное отображение единиц измерения после получения данных от бэкенда 1575
def test_03(page):
    def route_handler(route):
        fulfill_route(route, fill_response(1575, 1575, 1575))

    page.route(api_url, route_handler)

    page.goto(page_url, timeout=120000)

    page.locator('.desktop-impact-item-eeQO3').nth(1).screenshot(path="output/03_co2.png")
    page.locator('.desktop-impact-item-eeQO3').nth(3).screenshot(path="output/03_water.png")
    page.locator('.desktop-impact-item-eeQO3').nth(5).screenshot(path="output/03_energy.png")

# 4. Проверка конвертации значения с плавающей точкой 1200.85
def test_04(page):
    def route_handler(route):
        fulfill_route(route, fill_response(1200.85, 1200.85, 1200.85))

    page.route(api_url, route_handler)

    page.goto(page_url, timeout=120000)

    page.locator('.desktop-impact-item-eeQO3').nth(1).screenshot(path="output/04_co2.png")
    page.locator('.desktop-impact-item-eeQO3').nth(3).screenshot(path="output/04_water.png")
    page.locator('.desktop-impact-item-eeQO3').nth(5).screenshot(path="output/04_energy.png")    

# 5. Проверка отображения значений счётчиков после получения большого значения 9999999
def test_05(page):
    def route_handler(route):
        fulfill_route(route, fill_response(9999999, 9999999, 9999999))

    page.route(api_url, route_handler)

    page.goto(page_url, timeout=120000)

    page.locator('.desktop-impact-item-eeQO3').nth(1).screenshot(path="output/05_co2.png")
    page.locator('.desktop-impact-item-eeQO3').nth(3).screenshot(path="output/05_water.png")
    page.locator('.desktop-impact-item-eeQO3').nth(5).screenshot(path="output/05_energy.png")

# 6. Проверка отображения значений счётчиков после получения отрицательного значения от бэкенда -575
def test_06(page):
    def route_handler(route):
        fulfill_route(route, fill_response(-575, -575, -575))

    page.route(api_url, route_handler)

    page.goto(page_url, timeout=120000)

    page.locator('.desktop-impact-item-eeQO3').nth(1).screenshot(path="output/06_co2.png")
    page.locator('.desktop-impact-item-eeQO3').nth(3).screenshot(path="output/06_water.png")
    page.locator('.desktop-impact-item-eeQO3').nth(5).screenshot(path="output/06_energy.png")

# 7. Проверка отображения значений счётчиков после получения отрицательного значения от бэкенда null
def test_07(page):
    def route_handler(route):
        fulfill_route(route, fill_response(None, None, None))

    page.route(api_url, route_handler)

    page.goto(page_url, timeout=120000)

    page.locator('.desktop-impact-item-eeQO3').nth(1).screenshot(path="output/07_co2.png")
    page.locator('.desktop-impact-item-eeQO3').nth(3).screenshot(path="output/07_water.png")
    page.locator('.desktop-impact-item-eeQO3').nth(5).screenshot(path="output/07_energy.png")

# 8. Проверка отображения значений счётчиков после получения некорректных типов данных - строка "авито"
def test_08(page):
    def route_handler(route):
        fulfill_route(route, fill_response("авито", "авито" ,"авито"))

    page.route(api_url, route_handler)

    page.goto(page_url, timeout=120000)

    page.locator('.desktop-impact-item-eeQO3').nth(1).screenshot(path="output/08_co2.png")
    page.locator('.desktop-impact-item-eeQO3').nth(3).screenshot(path="output/08_water.png")
    page.locator('.desktop-impact-item-eeQO3').nth(5).screenshot(path="output/08_energy.png")