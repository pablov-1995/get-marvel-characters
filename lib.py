import requests
import time
import logging
import time
from hashlib import md5
import os

from utils import run_function_with_multiprocessing

def fetch_characters_chunk(args: tuple[str]) -> list:
    """
    Fetch a chunk of characters from the Marvel API.

    Args:
        args (tuple): Tuple containing arguments for fetching characters.
    
    Returns:
        list: List of dictionaries containing character names and their comic counts.
    """
    public_key, private_key, url, characters_endpoint, offset, limit = args
    ts = str(time.time())
    characters_url_endpoint = f"{url}/{characters_endpoint}"

    params = build_request_params(ts, public_key, private_key, limit, offset)

    try:
        response = requests.get(characters_url_endpoint, params=params)
        response.raise_for_status()
        data = response.json()['data']['results']
        return build_characters(data)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching characters at offset {offset}: {str(e)}")
        return []

def get_characters(
        public_key: str, 
        private_key: str, 
        url: str, 
        characters_endpoint: str, 
        limit: int = 100, 
        use_multiprocessing = True
    ) -> list[dict[str, str]]:
    """
    Get Marvel characters and their comic counts with pagination using multiprocessing.

    Args:
        public_key (str): Marvel API public key.
        private_key (str): Marvel API private key.
        url (str): Base URL for the Marvel API.
        characters_endpoint (str): Endpoint for fetching characters
        limit (int, optional): Number of results to fetch per request. Maximum as of now is 100 characters.
        use_multiprocessing (bool, optional): Flag to enable or disable multiprocessing.

    Returns:
        list: List of dictionaries containing character names and their comic counts.
    """
    logging.info("Fetching characters from Marvel API...")
    characters_url_endpoint = f"{url}/{characters_endpoint}"

    # Get total number of characters
    ts = str(time.time())
    params = build_request_params(ts, public_key, private_key, 1, 0)
    response = requests.get(characters_url_endpoint, params=params)
    response.raise_for_status()
    total_characters = response.json()['data']['total']

    # Calculate number of chunks
    num_chunks = (total_characters + limit - 1) // limit

    # Prepare arguments for multiprocessing
    args_list = [(public_key, private_key, url, characters_endpoint, i * limit, limit) for i in range(num_chunks)]

    if use_multiprocessing:
        results = run_function_with_multiprocessing(processes=os.cpu_count(), function=fetch_characters_chunk, args=args_list)
    else:
        results = [fetch_characters_chunk(arg) for arg in args_list]

    # Flatten the results
    characters = [character for chunk in results for character in chunk]

    return characters

def build_characters(data: list[dict[str]]) -> list[dict[str]]:
    """
    Build a list of characters with their comic counts.

    Args:
        data (list): List of dictionaries containing character data.
    
    Returns:
        list: List of dictionaries containing character names and their comic counts.
    """
    characters = []

    for character in data:
        character_name = character['name']
        comic_count = character['comics']['available']
        characters.append({'character_name': character_name, 'comic_count': comic_count})
    
    return characters

def build_request_params(
        ts: str, 
        public_key: str, 
        private_key: str, 
        limit: int, 
        offset: int
    ) -> dict[str, str]:
    """
    Build request parameters for fetching characters from the Marvel API.

    Args:
        ts (str): Current timestamp.
        public_key (str): Marvel API public key.
        private_key (str): Marvel API private key.
        limit (int): Number of results to fetch per request.
        offset (int): Offset for pagination.
    
    Returns:
        dict: Dictionary containing request parameters.
    """
    return {
        'ts': ts,
        'apikey': public_key,
        'hash': md5(f"{ts}{private_key}{public_key}".encode("utf8")).hexdigest(),
        'limit': limit,
        'offset': offset
    }