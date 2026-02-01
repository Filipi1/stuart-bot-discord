from abc import ABC, abstractmethod
from http import HTTPMethod
from typing import Optional, Dict, Any, Tuple


class HttpAdapter(ABC):
    @abstractmethod
    async def request(
        self,
        path: str,
        method: HTTPMethod,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        body: Optional[dict] = None,
    ) -> Dict[str, Any]:
        raise NotImplementedError()

    @abstractmethod
    async def request_multipart(
        self,
        path: str,
        method: HTTPMethod,
        data: Dict[str, str],
        files: Dict[str, Tuple[str, bytes, str]],
        headers: Optional[dict] = None,
    ) -> Dict[str, Any]:
        raise NotImplementedError()

    @abstractmethod
    async def request_image_bytes(
        self,
        url: str,
    ) -> bytes:
        raise NotImplementedError()
