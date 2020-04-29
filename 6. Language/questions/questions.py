import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    file_dict = {}
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename)) as file:
            txt = file.read()
            file_dict[filename] = txt

    return file_dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    all_words = nltk.word_tokenize(document)

    all_words = [w.lower() for w in all_words]

    words = []
    stopwords = nltk.corpus.stopwords.words("english")
    for w in all_words:
        punct = [c for c in w if c not in string.punctuation]
        if len(punct) > 0 and w not in stopwords:
            words.append(w)


    words.sort()

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    n_docs = len(documents)
    all_words = set()

    for doc in documents.keys():
        all_words = all_words.union(set(documents[doc]))

    idf_dict = {}
    for word in all_words:
        count = doc_word_count(word, documents)

        idf_dict[word] = math.log(n_docs / count)


    return idf_dict

def doc_word_count(word, documents):
    count = 0
    for doc, words in documents.items():
        if word in words:
            count += 1
    return count


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    file_tfidf = {}
    for file, words in files.items():
        tfidf = 0
        for w in query:
            if w in words:
                tf = words.count(w)
                tfidf += tf * idfs.get(w, 0)
        file_tfidf[file] = tfidf

    top_n_files = sorted(file_tfidf, key = file_tfidf.get, reverse = True)[0:n]


    return top_n_files



def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """


    idf_sent = {}
    hqtd_sent = {}
    for sent, words in sentences.items():

        idf = 0
        count = 0
        for w in query:
            if w in words:
                count += words.count(w)
                idf += idfs.get(w, 0)

        idf_sent[sent] = idf
        hqtd_sent[sent] = count / len(words)


    sorted_idf = sorted(idf_sent, key = idf_sent.get, reverse = True)

    while True:
        for i in range(len(sorted_idf)):
            s1 = sorted_idf[i]
            s2 = sorted_idf[i+1]
            if idf_sent[s1] == idf_sent[s2]:
                if hqtd_sent[s1] < hqtd_sent[s2]:
                    sorted_idf[i] = s2
                    sorted_idf[i+1] = s1
                    break
            elif i > n + 1:
                break
        break

    top_n_idf = sorted_idf[0:n]

    return top_n_idf





if __name__ == "__main__":
    main()
