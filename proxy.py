import random
from typing import List

import requests


class Proxy:
    @classmethod
    def get_http_proxy_list(cls, top: int = 10) -> List[str]:
        """
        Возвращает список http прокси, получая их из сервиса proxy_py.
        """
        proxies_url = 'http://158.101.192.82:55555/api/v1/'
        json_data = {
            "model": "proxy",
            "method": "get",
            "order_by": "response_time, uptime"
        }
        response = requests.post(proxies_url, json=json_data)
        if response.status_code == 200:
            return [f'{proxy["domain"]}:{proxy["port"]}' for proxy in response.json()['data'] if
                    proxy['protocol'] == 'http'][:top]
        else:
            raise ConnectionError

    @classmethod
    def get_random_http_proxy(cls, from_top: int = 10) -> str:
        """
        Возвращает случайный http прокси из списка прокси, полученных методом get_http_proxy_list.
        """
        return random.choice(Proxy.get_http_proxy_list(top=from_top))

    @classmethod
    def get_proxy_dict_for_requests(cls, proxy: str) -> dict:
        """
        Возвращает словарь для использования в качестве параметра proxies при запросах библиотеки requests.
        """
        if proxy:
            return {
                "http": 'http://' + proxy,
                "https": 'http://' + proxy,
            }

    @classmethod
    def proxy_health(
            cls,
            proxy,
            timeout: int = 5,
            url: str = "https://aviasales.ru") -> bool:
        """
        Проверяет работоспособность прокси сервера, делая GET запрос по :url
        """
        try:
            return requests.get(url, proxies=cls.get_proxy_dict_for_requests(proxy), timeout=timeout).status_code == 200
        except (requests.exceptions.ProxyError, requests.exceptions.ConnectionError):
            return False

    @classmethod
    def get_serviceable_proxy(
            cls,
            from_top: int = 10,
            url: str = "https://aviasales.ru") -> str:
        """
        Перебирает случайные прокси из списка, проверяя их на жизнеспособность методом proxy_health и возвращает
        первый найденный работоспособный прокси.
        """
        while True:
            proxy = Proxy.get_random_http_proxy(from_top=from_top)
            if Proxy.proxy_health(proxy, url=url):
                return proxy
