import json
import asyncio
from typing import Union

from typing import List

from aiohttp import ClientResponse
import requests
import aiohttp


class TEIClient:
  def __init__(self, host: str = 'localhost', port: int = 3000, protocol: str = 'http') -> List[float]:
    self.host = host
    self.port = port
    self.base_url = f"{protocol}://{self.host}:{self.port}"
    self.health()

  async def embed(self, text: str, session: aiohttp.ClientSession = None) -> List[float]:
    headers = {"Content-Type": "application/json"}
    data = {"inputs": text}

    if session is None:
      async with aiohttp.ClientSession(self.base_url) as s:
        async with s.post("/embed", headers=headers, data=json.dumps(data)) as response:
          self._check_embed_errors(response)
          return (await response.json())[0]
    else:
      async with session.post("/embed", headers=headers, data=json.dumps(data)) as response:
        self._check_embed_errors(response)
        return (await response.json())[0]

  async def embed_batch(self, texts: List[str]) -> List[List[float]]:
    async with aiohttp.ClientSession(self.base_url) as s:
      embeddings = await asyncio.gather(*[self.embed(text, s) for text in texts])
      return embeddings

  def health(self) -> bool:
    response = requests.get(f"{self.base_url}/health")
    response.raise_for_status()
    return True

  def embed_batch_sync(self, texts: List[str]) -> List[List[float]]:
    """Embeds a batch of texts with blocking.
    Args:
        texts (List[str]): list of texts to embed
    Returns:
        List[List[float]]: list of embeddings
    """
    return asyncio.run(self.embed_batch(texts))

  def embed_sync(self, text: str) -> List[float]:
    headers = {"Content-Type": "application/json"}
    data = {"inputs": text}
    response = requests.post(
        f"{self.base_url}/embed", headers=headers, data=json.dumps(data))
    self._check_embed_errors(response)
    return response.json()[0]

  def _check_embed_errors(self, response: Union[requests.Response, aiohttp.ClientResponse]) -> None:
    status = response.status_code if isinstance(
        response, requests.Response) else response.status
    if status != 200:
      try:
        error = response.json()
        raise RuntimeError(f"{error['error']} ({error['error_type']})")
      except Exception as e:
        if status == 413:
          raise RuntimeError("Batch size error") from e
        if status == 422:
          raise RuntimeError("Tokenization error") from e
        if status == 424:
          raise RuntimeError("Inference failed") from e
        if status == 429:
          raise RuntimeError("Model is overloaded") from e
        response.raise_for_status()

  def info(self) -> dict:
    response = requests.get(f"{self.base_url}/info")
    response.raise_for_status()
    return response.json()

  def metrics(self) -> dict:
    response = requests.get(f"{self.base_url}/metrics")
    response.raise_for_status()
    return response.text
