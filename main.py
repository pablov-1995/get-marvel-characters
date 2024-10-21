"""Main script to fetch Marvel characters and their comic counts."""

import logging
import time
import os
import json
from dotenv import load_dotenv
import argparse

from lib import get_characters
from utils import save_as_json, save_as_csv

# Load environment variables
load_dotenv()

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(
        use_multiprocessing: bool, 
        output_format: str, 
        file_name: str
    ):
    """
    Main function to fetch Marvel characters and their comic counts.

    Args:
        use_multiprocessing (bool): Flag to enable or disable multiprocessing.
        output_format (str): Output format for saving characters data.
        file_name (str): File name for saving characters data.
    """
    # set timestamp for start date
    start_time = time.time()
    logging.info(f'Starting Marvel character data fetch')

    # Load env variables
    url = os.getenv('MARVEL_API_URL')
    characters_endpoint = os.getenv('MARVEL_API_CHARACTERS_ENDPOINT')
    public_key = os.getenv('MARVEL_API_PUBLIC_KEY')
    private_key = os.getenv('MARVEL_API_PRIVATE_KEY')

    for key in [url, characters_endpoint, public_key, private_key]:
        if not key:
            logging.error("Failed to load {key} from environment variables.")
            return
    
    # Fetch characters and their comic counts using loaded keys
    logging.info(f'Using multiprocessing: {use_multiprocessing}')
    characters = get_characters(public_key, private_key, url, characters_endpoint, use_multiprocessing=use_multiprocessing)

    if len(characters) > 0:
        logging.info("Characters fetched successfully.")

        # Save file
        if output_format == 'json':
            save_as_json(characters, file_name)
        
        elif output_format == 'csv':
            save_as_csv(characters, file_name)

    else:
        logging.warning(f'No data fetched. {output_format} export skipped.')
    
    end_time = time.time()
    logging.info(f'Total execution time: {end_time - start_time}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch Marvel characters and their comic counts.')
    parser.add_argument('--use_multiprocessing', '-mp', help='Use multiprocessing for fetching characters.')
    parser.add_argument('--output_format', '-f', help='Output format for saving characters data.')
    parser.add_argument('--file_name', '-fn', help='File name for saving characters data.')

    args = parser.parse_args()

    if args.use_multiprocessing == 'True':
        args.use_multiprocessing = True
    elif args.use_multiprocessing == 'False':
        args.use_multiprocessing = False
    elif args.use_multiprocessing is None:
        args.use_multiprocessing = False
    else:
        logging.error("Invalid value for use_multiprocessing. Please provide either True or False.")
    
    if args.output_format not in ['json', 'csv'] and args.output_format is not None:
        logging.error("Invalid value for output_format. Please provide either json or csv.")

    main(
        use_multiprocessing=bool(args.use_multiprocessing), 
        output_format=args.output_format if args.output_format else 'csv', 
        file_name=args.file_name if args.file_name else 'marvel_output'
    )
