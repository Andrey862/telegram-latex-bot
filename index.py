from unidecode import unidecode
from collections import Counter
from latex_dict import all_modules
import vptree

weight_tri = 4
weight_two = 2
weight_one = 1

def preprocess(text: str) -> dict:
    # N-gram based search
    text = unidecode(text).lower()
    #text = '^' + text  + '$'
    text = text
    res = {}
    res['tri'] = dict(Counter([text[i:i+3] for i in range(len(text)-2)]))
    res['two'] = dict(Counter([text[i:i+2] for i in range(len(text)-1)]))
    res['one'] = dict(Counter([text[i:i+1] for i in range(len(text)-0)]))
    res['l'] = len(res['tri'])*weight_tri + len(res['two'])*weight_two + len(res['one'])*weight_one
    res['text'] = text
    return res


def similarity(item_1: dict, item_2: dict) -> float:
    res = 0
    res += weight_tri * sum(min(item_1['tri'][e], item_2['tri'][e])
                 for e in item_1['tri'].keys() & item_2['tri'].keys())
    
    res += weight_two * sum(min(item_1['two'][e], item_2['two'][e])
               for e in item_1['two'].keys() & item_2['two'].keys())
    
    res += weight_one * sum(min(item_1['one'][e], item_2['one'][e])
               for e in item_1['one'].keys() & item_2['one'].keys())
    
    res /= max(item_2['l'], item_1['l'])
    return res

index = None

def generate_tree():
    global index
    data = [preprocess('\\'+e) for e in all_modules.keys()]
    data.append(preprocess('\\frac'))
    index = vptree.VPTree(data, lambda p1, p2: 1 - similarity(p1,p2))

def search_command(query, n_neighbors=10):
    return [e[1]['text'] for e in index.get_n_nearest_neighbors(preprocess('\\'+query), n_neighbors)]

generate_tree()