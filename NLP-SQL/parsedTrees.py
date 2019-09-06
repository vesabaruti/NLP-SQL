from nltk.parse import CoreNLPParser
from graphviz import Source


def generateTree():
    sentence = 'Show me the students who scored less then 9'

    sdp = CoreNLPParser()
    result = list(sdp.raw_parse(sentence))

    printable_tree = [parse for parse in result][0]
    #printable_tree.pretty_print()
    printable_tree.draw()
    print(sentence)
    #return printable_tree

#generateTree()