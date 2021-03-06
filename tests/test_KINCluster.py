# -*- coding: utf-8 -*-
"""
    tests.KINCluster
    ---------------
    Test KINCluster
    :author: MaybeS(maytryark@gmail.com)
"""

import pytest

from KINCluster.core.cluster import Cluster 
from KINCluster.core.pipeline import Pipeline 
from KINCluster.core.extractor import Extractor 
from KINCluster.core.item import Item
from KINCluster.lib.tokenizer import tokenize, stemize

import codecs

test_text = ['2016헌나1.txt', '2014헌나1.txt']
test_keyword = ['헌법판결문', '헌법판결문']
# test_text = ['small.txt', 'small.txt']
# test_keyword = ['언어', '언어']

# Test1
class PipelineFile(Pipeline):
    def capture_item(self):
        for text, keyword in zip(test_text, test_keyword):
            with codecs.open('tests/data/' + text, 'r', 'utf-8') as f:
                content = f.read()
            yield Item(title=text,content=content,keyword=keyword,date='')

def test_app1():
    """ Testing for cluster, using test data
    """
    cluster = Cluster(epoch=32, tokenizer="stemize")
    pipeline = PipelineFile()

    for item in pipeline.capture_item():
        cluster.put_item(item)
    cluster.cluster()

    extractor = Extractor(cluster)
    for idx, dump in enumerate(cluster.dumps):
        items, vectors, counter = list(map(list, list(zip(*dump))))

        extracted = extractor.dump(idx)

        assert isinstance(extracted.keywords, list)
        pipeline.dress_item(extracted)

# Test3
import pandas as pd
from nltk import ngrams
test_csv = 'tests/data/test.csv'

class PipelineCsv(Pipeline):
    def __init__(self, csv):
        self.frame = pd.read_csv(csv)
    def capture_item(self):
        for idx, row in self.frame.iterrows():
            yield Item(title=row.title,content=row.content,keyword=row.actor,date=row.date)
    def dress_item(self, extracted):
        pass

def test_app3():
    """ Testing for cluster, using test data
    """
    cluster = Cluster(tokenizer="tokenize")
    pipe = PipelineCsv(test_csv)

    for item in pipe.capture_item():
        cluster.put_item(item)
    cluster.cluster()

    extractor = Extractor(cluster)
    for idx, dump in enumerate(cluster.dumps):
        items, vectors, counter = list(map(list, list(zip(*dump))))
        extracted = extractor.dump(idx)

        pipe.dress_item(extracted)
    print((cluster.distribution))