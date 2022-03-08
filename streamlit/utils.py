import sys
import time
import streamlit as st
from elasticsearch import exceptions

def check_and_create_index(es, index: str):
    """ checks if index exits and loads the data accordingly """
    mappings = {
        'mappings': {
            'properties': {
                'name': {'type': 'text'},
                'date': {'type': 'keyword'},
                'citation': {'type': 'text'},
                'tags': {'type': 'keyword'},
                'content': {'type': 'text'},
            }
        }
    }
    if not safe_check_index(es, index):
        print(f'Index {index} not found. Create a new one...')
        es.indices.create(index=index, body=mappings, ignore=400)


def safe_check_index(es, index: str, retry: int = 3):
    """ connect to ES with retry """
    if not retry:
        print('Out of retries. Bailing out...')
        sys.exit(1)
    try:
        status = es.indices.exists(index)
        return status
    except exceptions.ConnectionError as e:
        print('Unable to connect to ES. Retrying in 5 secs...')
        time.sleep(5)
        safe_check_index(es, index, retry - 1)

@st.experimental_memo
def index_search(_es, index: str, keywords: str, filters: str, from_i: int,
                 size: int) -> dict:
    """ """
    body = {
        'query': {
            'bool': {
                'must': [
                    {
                        'query_string': {
                            'query': keywords,
                            'fields': ['content'],
                            'default_operator': 'AND',
                        }
                    }
                ],
            }
        },
        'highlight': {
            'pre_tags': ['<b>'],
            'post_tags': ['</b>'],
            'fields': {'content': {}}
        },
        'from': from_i,
        'size': size,
        'aggs': {
            'tags': {
                'terms': {'field': 'tags'}
            },
            'match_count': {'value_count': {'field': '_id'}}
        }
    }
    if filters is not None:
        body['query']['bool']['filter'] = {
            'terms': {
                'tags': [filters]
            }
        }

    res = _es.search(index=index, body=body)
    # sort popular tags
    sorted_tags = res['aggregations']['tags']['buckets']
    sorted_tags = sorted(sorted_tags, key=lambda t: t['doc_count'], reverse=True)
    res['sorted_tags'] = [t['key'] for t in sorted_tags]
    return res


def index_cases(es, index: str, cases: dict, test:bool):
    """ """
    with st.spinner(f'Indexing...'):
        success = 0
        for url, case in cases.items():
            _case = case.copy()
            _case['content'] = f"{_case['name']} {' '.join(_case['content'])}"
            es.index(index=index, id=url, body=_case)
            cases[url] = {'success': True, **_case}
            success += 1
            #except:
            #    cases[url] = {'success': False, **_case}

    if test == True:
        st.subheader('Results')
        st.write(f'Total={len(cases)}, {success} succeed, {len(cases) - success} failed.')
        st.write(cases)


@st.cache(show_spinner=False)
def shorten_title(title: str, limit: int = 65) -> str:
    """ Shorten the title of a story. """
    if len(title) > limit:
        title = title[:limit] + '...'

    return title


@st.cache(show_spinner=False)
def simplify_es_result(result: dict) -> dict:
    """ """
    res = result['_source']
    res['index'] = result['_id']
    # join list of highlights into a sentence
    res['highlights'] = '...'.join(result['highlight']['content'])
    # limit the number of characters in the title
    res['name'] = shorten_title(res['name'])
    return res