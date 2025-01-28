import httpx
import requests

SEARCH_ENGINES = {
    "IndexNow": "https://api.indexnow.org/indexnow",
    "Bing": "https://www.bing.com/indexnow",
    "Naver": "https://searchadvisor.naver.com/indexnow",
    "Seznam": "https://search.seznam.cz/indexnow",
    "Yandex": "https://yandex.com/indexnow",
    "Yep": "https://indexnow.yep.com/indexnow",
}

class IndexNow:
    def __init__(self, key: str, host: str) -> None:
        self.key = key
        self.host = host
        self.search_engines = SEARCH_ENGINES

    def get_json(self, url: str) -> dict:
        return {
                'host': self.host,
                'key': self.key,
                'keyLocation': f'https://{self.host}/{self.key}.txt',
                'urlList':[
                    url
                ]
                }
    
    async def async_add_to_index(self, url: str) -> list[httpx.Response]:
        """
        HTTP Response Codes for IndexNow API:

        - 200 OK:
            URL submitted successfully.
        
        - 202 Accepted:
            URL received. IndexNow key validation pending.
        
        - 400 Bad Request:
            Invalid format in the request.
        
        - 403 Forbidden:
            The key is not valid (e.g. key not found, file found but key not in the file).
        
        - 422 Unprocessable Entity:
            URLs that don’t belong to the host or the key does not match the schema in the protocol.
        
        - 429 Too Many Requests:
            Too many requests, potential spam detected.
        """
        json = self.get_json(url)
        async_client = httpx.AsyncClient()
        responses = []
        for search_engine_key in self.search_engines:
            response = await async_client.post(
                self.search_engines[search_engine_key],
                headers={'Content-Type': 'application/json', 'charset': 'utf-8'},
                json=json
            )
            responses.append(response)
        return responses
        
    def add_to_index(self, url: str) -> list[requests.Response]:
        """
        HTTP Response Codes for IndexNow API: See the docstring for the method async_add_to_index.
        """
        json = self.get_json(url)
        session = requests.Session()
        responses = []
        for search_engine_key in self.search_engines:
            response = session.post(
                self.search_engines[search_engine_key], 
                headers={'Content-Type': 'application/json', 'charset': 'utf-8'},
                json=json
            )
            responses.append(response)
        return responses