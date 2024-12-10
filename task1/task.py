import json
import sys

def get_nested_value(data, keys):
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            raise KeyError(f"Key '{key}' not found.")
    return data

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <path_to_json> <key1> <key2> ... <keyN>")
        return

    file_path = sys.argv[1]
    keys = sys.argv[2:]

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            
        keys = [key if key.isdigit() else key for key in keys]

        value = get_nested_value(data, keys)
        print(value)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except KeyError as e:
        print(e)
    except json.JSONDecodeError:
        print("Invalid JSON file format.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
