from http import HTTPMethod
from typing import Dict, Optional, Any
import requests
from requests.exceptions import RequestException

from modules.shared.adapters.http.http_adapter import HttpAdapter
from modules.shared.services.requests.exceptions import HttpException
from modules.shared.services.logger import LoggerService


class RequestsService(HttpAdapter):
    def __init__(self, base_url: str, context: Optional[str] = None):
        self.__base_url = base_url
        self.__logger = LoggerService(context or RequestsService.__name__)
        super().__init__()

    async def request(
        self,
        path: str,
        method: HTTPMethod,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        body: Optional[dict] = None,
    ) -> Dict[str, Any]:
        url = f"{self.__base_url}{path}"
        try:

            match method:
                case HTTPMethod.GET:
                    response = requests.get(
                        url, headers=headers, params=params, json=body
                    )
                case HTTPMethod.POST:
                    response = requests.post(
                        url, headers=headers, params=params, json=body
                    )
                case _:
                    raise NotImplementedError(f"Método HTTP {method} não implementado")

            return self.__get_response(response)

        except RequestException as request_error:
            self.__logger.error(f"Erro na requisição: {request_error}")
            raise request_error

    def __get_response(self, response: requests.Response) -> Dict[str, Any]:
        if 200 <= response.status_code <= 299:
            return response.json()
        return self.__exception_handler(response)

    def __exception_handler(self, response: requests.Response) -> None:
        self.__logger.dict_to_table(response.json())
        result = response.text
        self.__logger.error(f"[{response.status_code}] Request failed: {result}")
        raise HttpException(response.status_code, result)
