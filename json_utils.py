import json
import pandas as pd
import os
from typing import Union, Dict, Any


def load_json_file(file_path: str) -> Union[Dict[str, Any], list]:
    """
    Load JSON data from a file.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        dict or list: Parsed JSON data
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file is not valid JSON
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Check file size (24MB limit)
    file_size = os.path.getsize(file_path)
    max_size = 24 * 1024 * 1024  # 24MB in bytes
    if file_size > max_size:
        raise ValueError(f"File size exceeds 24MB limit. File size: {file_size / (1024*1024):.2f}MB")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON format: {str(e)}", e.doc, e.pos)


def json_to_dataframe(json_data: Union[Dict[str, Any], list]) -> pd.DataFrame:
    """
    Convert JSON data to a pandas DataFrame.
    
    Args:
        json_data (dict or list): JSON data to convert
        
    Returns:
        pd.DataFrame: DataFrame representation of the JSON data
    """
    try:
        # If it's a dictionary with nested data, we might need to normalize it
        if isinstance(json_data, dict):
            # Check if it's a simple dict or a nested structure
            df = pd.json_normalize(json_data)
        else:
            # If it's a list, convert directly
            df = pd.json_normalize(json_data)
        return df
    except Exception as e:
        raise ValueError(f"Could not convert JSON to DataFrame: {str(e)}")


def get_json_structure(data: Union[Dict, list], path: str = "") -> dict:
    """
    Analyze the structure of JSON data.
    
    Args:
        data (dict or list): JSON data to analyze
        path (str): Current path in the JSON structure (for recursion)
        
    Returns:
        dict: Structure information of the JSON data
    """
    structure = {}
    
    if isinstance(data, dict):
        structure['type'] = 'object'
        structure['properties'] = {}
        structure['size'] = len(data)
        
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            if isinstance(value, dict):
                structure['properties'][key] = get_json_structure(value, current_path)
            elif isinstance(value, list):
                structure['properties'][key] = {'type': 'array', 'size': len(value)}
                if len(value) > 0 and isinstance(value[0], dict):
                    structure['properties'][key]['items'] = get_json_structure(value[0], current_path + "[0]")
            else:
                structure['properties'][key] = {'type': type(value).__name__}
                
    elif isinstance(data, list):
        structure['type'] = 'array'
        structure['size'] = len(data)
        if len(data) > 0:
            if isinstance(data[0], dict):
                structure['items'] = get_json_structure(data[0], path + "[0]")
            else:
                structure['items'] = {'type': type(data[0]).__name__}
                
    else:
        structure['type'] = type(data).__name__
        
    return structure


def validate_json_format(file_path: str) -> bool:
    """
    Validate if a file contains valid JSON.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        bool: True if valid JSON, False otherwise
    """
    try:
        load_json_file(file_path)
        return True
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return False