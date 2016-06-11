import numpy as np
import pandas as pd
from collections import defaultdict, Counter


class Vocab(object):
    '''
    Vocab stores the words and their distributions to be used 
    in writing a poem

    '''

    def __init__(self, infile):
        self.word_source = self.make_word_source(infile)
        #self.word_count = Counter()
        self.word_count = self.get_word_count()
        self.next_words = defaultdict(dict)

    def make_word_source(self, infile):
        with open(infile) as f:
            return f.read()

    def add_next_word(self, current_word, next_word):
        if next_word in self.next_words[current_word]:
            self.next_words[current_word][next_word] += 1
        else:
            self.next_words[current_word][next_word] = 1
    def get_word_count(self):
        word_count = Counter(self.word_source.lower().split())
        return word_count
    
    def update_word_count(self, current_word):
        self.word_count[current_word] += 1

    

class Poem(object):
    '''
    Poem class uses Vocab class to build a poem

    '''

    def __init__(self, vocab):
        self.poem = []
        self.length = 0
        self.vocab = vocab

    def choose_first_word(self, vocab):
        first_word = None
        word_list = [k for k in vocab.word_count]
        while first_word is None:

            new_word = np.random.choice(word_list)
            if new_word in vocab.next_words:
                first_word = new_word
        self.write_word(first_word)
        self.length += 1
        return first_word

    def choose_new_word(self, vocab):
        new_word = None
        current_word = self.poem[-1]
        possible_words = [k for k in vocab.next_words[current_word]]
        possible_words_counts = np.array([vocab.next_words[current_word][k] for k in possible_words])
        possible_words_probs = np.true_divide(possible_words_counts, np.sum(possible_words_counts))
        while new_word is None:
            new_next_word = np.random.choice(possible_words, p=possible_words_probs)
            if len(vocab.next_words[new_next_word]) > 0:
                '''this test should make sure that the word to be added is a key in vocab.next_words
                '''
                new_word = new_next_word
                self.write_word(new_word)
                self.length += 1
            else:
                new_word = self.choose_first_word(vocab)
        
    def write_word(self, word):
        self.poem.append(word)



    

if __name__ == '__main__':
    infile = 'poem1.txt'
    vocabulary = Vocab(infile)
    with open('poem1.txt') as f:
        text = [row.lower().split() for row in f]
    for line in text:
        next_words = defaultdict(int)
        num_words = len(line)
        for idx, word in enumerate(line):
            if idx < num_words -1:
                vocabulary.add_next_word(word, line[idx+1])

    poem = Poem(vocabulary) 
    poem.choose_first_word(vocabulary)
    p_length = np.random.randint(10,19)
    while poem.length < p_length :
        poem.choose_new_word(vocabulary)
    
    print " ".join(poem.poem)

