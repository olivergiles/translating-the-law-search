import json
import gcsfs

def open_from_bucket():
    gcs_file_system = gcsfs.GCSFileSystem()
    gcs_json_path = "gs://law-data-ogiles/data/simplified_data.json"
    with gcs_file_system.open(gcs_json_path) as f:
        json_dict = json.load(f)
    data = eval(json_dict)
    clean_data = [case for case in data if not case["press summary"].get('error')]
    new_data = clean_data[8:40] + clean_data[104:894]
    return new_data

def create_search_data(data):
    search_data = {}
    for i, case in enumerate(data):
        KEY = i
        data = {
            'name':case['details']['Name'],
            'date':case['details']['Judgment date'],
            'citation':case['details']['Neutral citation'],
            'tags': ["law", "judge", "case"],
            'content':[case['press summary']['Background to the appeal'][:150],
                       case['press summary']['Reasons for the judgment'][:150],
                       case['details']['Neutral citation'],
                       case['details']['Judgment date'],
                       case['details']['Justices']
                       ]
        }
        search_data[KEY] = data
    return search_data

def get_search_data():
    data = open_from_bucket()
    return create_search_data(data)