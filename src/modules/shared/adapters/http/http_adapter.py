from abc import ABC, abstractmethod
from http import HTTPMethod
from typing import Optional, Dict, Any


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
