import os
import re
import json
from collections import defaultdict

news_dir = './news'
count_threshold = 4

def read_files():
    words = {}
    for d in os.listdir(news_dir):
        sub_dir = os.path.join(news_dir, d)
        if os.path.isdir(sub_dir):
            words[d] = defaultdict(int)
            for f in os.listdir(sub_dir):
                file_map = {}
                file_path = os.path.join(sub_dir, f)
                contents = open(file_path).read()
                contents = re.compile('\w+').findall(contents)
                for word in contents:
                    file_map[word] = 1
                for word in file_map:
                    words[d][word] += 1
    return words

def get_distinct_words(words):
    distinct_words = defaultdict(dict)
    for category in words:
        remaining_category_words = set([])
        for cat in words:
            if cat != category:
                remaining_category_words.update(set(words[cat].keys()))
        category_words = words[category].keys()
        for word in category_words:
            if word not in remaining_category_words:
                distinct_words[category][word] = words[category][word]
    return distinct_words

def words_above_threshold(words):
    distinct_words = defaultdict(dict)
    for category in words:
        category_words = words[category].keys()
        for word in category_words:
            if words[category][word] >= count_threshold:
                distinct_words[category][word] = words[category][word]
    return distinct_words

def get_words_list():
    words = read_files()
    distinct_words = get_distinct_words(words) 
    distinct_words = words_above_threshold(distinct_words)
    return distinct_words


def write_to_files(words):
    for category in words:
        f = open(category, 'w+')
        f.write('\n'.join(words[category].keys()))
        f.close()

write_to_files(get_words_list())

