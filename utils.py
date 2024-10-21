import csv
import json
import multiprocessing
import os

def run_function_with_multiprocessing(function: callable, args: list[tuple], processes: int = os.cpu_count()) -> list:
    """
    Run a function with multiprocessing.

    Args:
        processes (int, optional): Number of processes to use for multiprocessing.
        function (callable): Function to run with multiprocessing.
        args (list): List of tuples containing arguments for the function.

    Returns:
        list: List of results from the function.
    """
    with multiprocessing.Pool(processes=processes) as pool:
        results = pool.map(function, args)
    
    return results

def save_as_json(objects: list, file_name: str):
    """Save a list of dictionaries as a JSON file."""
    with open(f'{file_name}.json', 'w') as f:
        f.write(json.dumps(objects))
    return

def save_as_csv(objects: list, file_name: str):
    """Save a list of dictionaries as a CSV file."""
    keys = objects[0].keys()
    with open(f'{file_name}.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(objects)
    return