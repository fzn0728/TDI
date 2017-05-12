
# coding: utf-8

# In[ ]:
'''

from mrjob.job import MRJob
from mrjob.step import MRStep
import re
import heapq

WORD_RE = re.compile(r"[\w']+")
n = 5

class MRMostUsedWord(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_words,
                   combiner=self.combiner_count_words,
                   reducer=self.reducer_count_words),
            MRStep(reducer=self.reducer_find_max_word)
        ]

    def mapper_get_words(self, _, line):
        # yield each word in the line
        for word in WORD_RE.findall(line):
            yield (word.lower(), 1)

    def combiner_count_words(self, word, counts):
        # optimization: sum the words we've seen so far
        yield (word, sum(counts))

    def reducer_count_words(self, word, counts):
        # send all (num_occurrences, word) pairs to the same reducer.
        # num_occurrences is so we can easily use Python's max() function.
        yield None, (-1 * sum(counts), word)

    def get_top_n(self, word_count_pairs):
        h = []
        output = []
        for word_pair in word_count_pairs:
            heapq.heappush(h, word_pair)
            
        for i in xrange(min(len(h), 2)):
            top = heapq.heappop(h)
            output.append((-1*top[0], top[1]))
        return output
        # return h

    # discard the key; it is just None
    def reducer_find_max_word(self, _, word_count_pairs):
        # each item of word_count_pairs is (count, word),
        # so yielding one results in key=counts, value=word
        ret = self.get_top_n(word_count_pairs)
        yield ret


if __name__ == '__main__':
    MRMostUsedWord.run()
'''

from mrjob.job import MRJob
from mrjob.step import MRStep
import re
import heapq

WORD_RE = re.compile(r"[\w']+")


class MRMostUsedWord(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_words,
                   combiner=self.combiner_count_words,
                   reducer=self.reducer_count_words),
            MRStep(reducer=self.reducer_find_max_word)
        ]

    def mapper_get_words(self, _, line):
        # yield each word in the line
        for word in WORD_RE.findall(line):
            yield (word.lower(), 1)

    def combiner_count_words(self, word, counts):
        # optimization: sum the words we've seen so far
        yield (word, sum(counts))

    def reducer_count_words(self, word, counts):
        # send all (num_occurrences, word) pairs to the same reducer.
        # num_occurrences is so we can easily use Python's max() function.
        yield None, (sum(counts), word)

    # discard the key; it is just None
    def reducer_find_max_word(self, _, word_count_pairs):
        # each item of word_count_pairs is (count, word),
        # so yielding one results in key=counts, value=word
        h = []
        output = []
        for word_pair in word_count_pairs:
            heapq.heappush(h, word_pair)
        # for i in range(3):
        #     top = heapq.heappop(h)
        #     output.append(top[0])
        # yield type(heapq.heappop(h))
        yield heapq.nlargest(2, word_count_pairs)

if __name__ == '__main__':
    MRMostUsedWord.run()