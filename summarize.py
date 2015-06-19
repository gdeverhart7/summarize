#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import codecs
from itertools import combinations
from operator import itemgetter

from distance import jaccard
from networkx import Graph, pagerank
from nltk import corpus, tokenize


def get_words(sentence, stopwords):
    return filter(
        lambda word: word not in stopwords and word.isalnum(),
        tokenize.word_tokenize(sentence))


def summarize(text, sentence_count=2, language='english'):
    stopwords = corpus.stopwords.words(language)
    sentence_list = tokenize.sent_tokenize(text, language)
    wordsets = [get_words(sentence, stopwords) for sentence in sentence_list]

    graph = Graph()
    pairs = combinations(enumerate(wordsets), 2)
    for (index_a, words_a), (index_b, words_b) in pairs:
        similarity = 1 - jaccard(words_a, words_b)
        if similarity > 0:
            graph.add_edge(index_a, index_b, weight=similarity)

    ranked_sentence_indexes = pagerank(graph).items()
    sentences_by_rank = sorted(
        ranked_sentence_indexes, key=itemgetter(1), reverse=True)
    best_sentences = map(itemgetter(0), sentences_by_rank[:sentence_count])
    best_sentences_in_order = sorted(best_sentences)

    return ' '.join(sentence_list[index] for index in best_sentences_in_order)


if __name__ == "__main__":
    filename = sys.argv[1]
    with codecs.open(filename, encoding='utf-8') as f:
        print summarize(f.read(), 5)