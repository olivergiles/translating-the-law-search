import json
import gcsfs

def open_from_bucket():
    gcs_file_system = gcsfs.GCSFileSystem()
    gcs_json_path = "gs://law-data-ogiles/data/simplified_data.json"
    with gcs_file_system.open(gcs_json_path) as f:
        json_dict = json.load(f)
    data = eval(json_dict)
    clean_data = [case for case in data if not case["press summary"].get('error')]
    return clean_data

def create_search_data(data):
    search_data = {}
    for i, case in enumerate(data):
        KEY = i
        data = {
            'name':case['details']['Name'],
            'date':case['details']['Judgment date'],
            'citation':case['details']['Neutral citation'],
            'tags': ["law", "judge", "case"],
            'content':[case['details']['Neutral citation'],
                       case['details']['Judgment date'],
                       case['press summary']['Reasons for the judgment'][:150]]
        }
        search_data[KEY] = data
    return search_data

def get_search_data():
    data = open_from_bucket()
    return create_search_data(data)