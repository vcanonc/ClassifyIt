import json
import os


def write(dictionary, file):
    """Write a given file a new dictionary.

    :param dictionary:
    :param file:
    :return:
    """
    path = os.path.dirname(__file__) + '\\' + file
    with open(path, 'w') as f:
        
        json.dump(dictionary, f, sort_keys=True)


def read(file):
    """Read json file and return dictionary data.

    :param file:
    :return json_data:
    """
    try:
        path = os.path.dirname(__file__) + '\\' + file
        with open(path, 'r') as f:
            json_data = json.load(f)
        return json_data
    except FileNotFoundError as e:
        print(f'ERROR: {e}')


def restore_config():
    """Write default data dictionary to configuration files (json)."""
    extensions = {
        "Documents": ['.docx', '.txt', '.doc', '.ods', '.pdf', '.pptx', '.ppt', '.tex', '.xls', '.xlsx', '.csv', '.odt'],
        "Images": ['.png', '.jpg', '.jpeg', '.gif', '.ico', '.bmp', '.svg'],
        "Audio": ['.mp3', '.wav', '.wma', '.ogg', '.flac', '.m4a'],
        "Video": ['.mov', '.mp4', '.avi', '.mkv', '.wmv'],
        "Executable": ['.exe', '.msi'],
        "Compressed": ['.rar', '.zip', '.7z', '.rar5']
    }
    keywords = {
        'Exam': ['exam', 'test', 'quiz']
    }
    write(extensions, 'config/extensions.json')
    write(keywords, 'config/keywords.json')
