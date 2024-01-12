import json
import jsonschema
import logging
import allure
import requests
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from aliexpress_ru.utils import load_schema
from selene import browser

base_url = 'https://aliexpress.ru'


def aliexpress_api_post(url, **kwargs):
    with step("API POST Request"):
        result = requests.post(url=base_url + url, **kwargs)

        allure.attach(body=result.request.url, name="Request url",
                      attachment_type=AttachmentType.TEXT)
        allure.attach(body=json.dumps(result.request.body, indent=4, ensure_ascii=True), name="Request body",
                      attachment_type=AttachmentType.JSON, extension="json")

        allure.attach(body=json.dumps(result.json(), indent=4, ensure_ascii=True), name="Response",
                      attachment_type=AttachmentType.JSON, extension="json")

        logging.info("Request: " + result.request.url)
        if result.request.body:
            logging.info("INFO Request body: " + result.request.body)
        logging.info("Request headers: " + str(result.request.headers))
        logging.info("Response code " + str(result.status_code))
        logging.info("Response: " + result.text)
    return result


def test_shopping_cart(browser_setup):

    schema = load_schema.load_path("shopping_cart.json")
    result = aliexpress_api_post('/aer-jsonapi/v2/cart/count')
    # cookie = result.cookies.get("JSESSIONID")

    # with step("Set cookie from API"):
    #     browser.open('https://aliexpress.ru/')
    #
    #     browser.driver.add_cookie({"name": "JSESSIONID", "value": cookie})
    #
    # with step("Open cart"):
    #     browser.open('https://shoppingcart.aliexpress.ru/shopcart/shopcartDetail.htm')

    with allure.step('Проверить, что API возвращает 200 код ответа'):
        assert result.status_code == 200
    with allure.step('Проверить, что в корзине пусто'):
        assert result.json().get('data').get('count') == 0
    with allure.step('Провалидировать схему ответа'):
        jsonschema.validate(result.json(), schema)


def test_shopping_cart_with_product(browser_setup):

    schema = load_schema.load_path("shopping_cart.json")
    result = aliexpress_api_post('/aer-jsonapi/v2/cart/items/add?_bx-v=2.5.8')
    # cookie = result.cookies.get("JSESSIONID")

    # with step("Set cookie from API"):
    #     browser.open('https://aliexess.ru/')
    #
    #     browser.driver.add_cookie({"name": "JSESSIONID", "value": cookie})
    #
    # with step("Open cart"):
    #     browser.open('https://shoppingcart.aliexpress.ru/shopcart/shopcartDetail.htm')

    with allure.step('Проверить, что API возвращает 200 код ответа'):
        assert result.status_code == 200
    with allure.step('Проверить, что в корзине 1 товар'):
        assert result.json().get('data').get('count') == 1
    with allure.step('Провалидировать схему ответа'):
        jsonschema.validate(result.json(), schema)




