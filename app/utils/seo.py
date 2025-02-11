from indexflow import IndexNow
from loguru import logger

from ..config.consts import SERVICE_NAME, INDEXNOW_KEY


async def add_index(page_url: str) -> None:
    """
    Asynchronously adds a page URL to the IndexNow API and logs the result.

    Parameters:
        -page_url : str
            - The URL to be submitted for indexing.

    Returns:
        - None
        
    In case of error, the function logs a failure message with the response details.
    """
    host = IndexNow.get_host_name(page_url, need_http=True)
    if INDEXNOW_KEY: 
        index_now = IndexNow(key=INDEXNOW_KEY, host=host)
        responses = await index_now.async_add_to_index(page_url)
    else:
        logger.warning("INDEXNOW_KEY is not set, skipping the IndexNow API")
        return
    for response in responses:
        if response.status_code not in (200, 202):
            logger.error(f"Failed to add {page_url} to the IndexNow API. Response server: {response}")
        else:
            logger.info(f"Successfully added {page_url} to the IndexNow API")

def sync_add_index(page_url: str) -> None:
    """
    Adds a page URL to the IndexNow API and logs the result.

    Parameters:
        -page_url : str
            - The URL to be submitted for indexing.

    Returns:
        - None
        
    In case of error, the function logs a failure message with the response details.
    """
    host = IndexNow.get_host_name(page_url, need_http=True)
    if INDEXNOW_KEY: 
        index_now = IndexNow(key=INDEXNOW_KEY, host=host)
        responses = index_now.add_to_index(page_url)
    else:
        logger.warning("INDEXNOW_KEY is not set, skipping the IndexNow API")
        return
    for response in responses:
        if response.status_code not in (200, 202):
            logger.error(f"Failed to add {page_url} to the IndexNow API. Response server: {response}")
        else:
            logger.info(f"Successfully added {page_url} to the IndexNow API")