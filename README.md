Implement a token- and lexicon-based NER. Its comparison takes place at word/token level without use of text.find(name).

1. read in the dictionary, store it as a set of tokens
    
2. traverse the tokenized text, for each token check if it is (name)candidate and check if other name components are in a predefined window around the found token.
    

## Error analysis

#TODO

## Data

- first.txt and last.txt, lists of first and last names
    
- test.sentences, selection of sentences from a news corpus
    
- test.names, names selected by experts for each sentence. This is the gold standard, i.e. the correct result (by definition).
    

## Packages used
NLTK, regex, csv, string
