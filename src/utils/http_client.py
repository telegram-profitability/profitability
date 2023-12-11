from abc import ABC
from abc import abstractmethod

import httpx


class AbstractHttpClient(ABC):
    @abstractmethod
    async def get(self, url: str, headers: dict = None, params: dict = None) -> dict | None:
        raise NotImplementedError()

    @abstractmethod
    async def post(self, url: str, headers: dict = None, json: dict = None) -> dict | None:
        raise NotImplementedError()


class HttpClient(AbstractHttpClient):
    async def get(self, url: str, headers: dict = None, params: dict = None) -> dict | None:
        if headers is None:
            headers = {}
        if params is None:
            params = {}

        async with httpx.AsyncClient() as client:
            response = await client.get(headers=headers, url=url, params=params)
            return response.json() if response.status_code == 200 else None

    async def post(self, url: str, headers: dict = None, json: dict = None) -> dict | None:
        if headers is None:
            headers = {}
        if json is None:
            json = {}

        async with httpx.AsyncClient() as client:
            response = await client.post(headers=headers, url=url, json=json)
            return response.json() if response.status_code == 200 else None
