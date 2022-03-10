import json
import gcsfs
from random import shuffle
from top2vec import Top2Vec
import os
import re

base_path = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_path, "model", "model_deep_L")
model_ttl = Top2Vec.load(model_path)

def cleaner(text, **kwargs):
  """params is a list of things to remove: codec, acronyms, numbers, brackets, page, para, legal formatting """
  if not 'params' in kwargs:
    kwargs['params'] = ['codec', 'acronyms', 'numbers', 'brackets', 'page', 'para', 'legal formatting', 'info']
  if 'codec' in kwargs['params']:
    text_encoded = text.encode('ascii', errors = 'ignore')
    text_decode = text_encoded.decode()
    clean_text = " ".join([word for word in text_decode.split()])
    text = clean_text
  if 'numbers' in kwargs['params']:
    pattern = r'[0-9]'
    text = re.sub(pattern, '', text)
  if 'brackets' in kwargs['params']:
    text = re.sub('\(.*?\)', '', text)
    text = re.sub('\[.*?\]', '', text)
  if 'acronyms' in kwargs['params']:
    text = text.split()
    clean_text = []
    for word in text:
      if any(l.islower() for l in word):
        clean_text.append(word)
    text = ' '.join(clean_text)
  if 'page' in kwargs['params']:
      text = re.sub('Page [0-9]+', '', text)
  if 'para' in kwargs['params']:
      text = re.sub('Para [0-9]+', '', text)
  if 'legal formatting' in kwargs['params']:
      text = re.sub('Civ', '', text)
      text = re.sub('On appeal from:', '', text)
  if 'info' in kwargs['params']:
      text = re.sub("NOTE.*", "", text)
  return text

def get_tag(lst_str):
    res = model_ttl.query_topics(query = lst_str, num_topics=1)
    return list(res[0][0][:3])

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
        tag_data = case['press summary']['Background to the appeal'][:100]
        data = {
            'name':case['details']['Name'],
            'date':case['details']['Judgment date'],
            'citation':case['details']['Neutral citation'],
            'tags': get_tag(tag_data),
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