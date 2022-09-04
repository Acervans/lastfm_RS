"""
Author: Doris Zhou, adapted to NRC-VAD by Javier Wang
Date: September 29, 2017
Performs sentiment analysis on a text file using NRC-VAD.
Parameters:
    --dir [path of directory]
        specifies directory of files to analyze
    --file [path of text file]
        specifies location of specific file to analyze
    --out [path of directory]
        specifies directory to create output files
    --mode [mode]
        takes either "median" or "mean"; determines which is used to calculate sentence sentiment values
"""
# add parameter to exclude duplicates? also mean or median analysis

from nltk.corpus import stopwords
from nltk import tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from stanfordcorenlp import StanfordCoreNLP
from dataclasses import dataclass, field
import csv
import sys
import os
import statistics
import time
import argparse

nlp = StanfordCoreNLP('../lib/stanford-corenlp-4.5.0')
stops = set(stopwords.words("english"))
nrc = "../data/NRC-VAD-Lexicon.csv"
lmtzr = WordNetLemmatizer()

# Open NRC-VAD and store as list of dictionaries
with open(nrc, encoding="utf-8-sig") as csvfile:
    reader = list(csv.DictReader(csvfile))


@dataclass
class TextVAD:
    """ Class containing data for VAD values
    """
    valence: float = -1
    arousal: float = -1
    dominance: float = -1
    label: str = field(init=False)

    # # optional
    # # maybe use lastfm ID as last_id, although the object should be
    # # linked to the song/album/artist in the first place
    # last_id: int = None
    # sentence: Optional[str] = None
    # found_words: list(str) = None
    # all_words: list(str) = None

    def __post_init__(self):
        # set sentiment label
        self.label = 'neutral'
        if self.valence > .55:
            self.label = 'positive'
        elif self.valence < .45:
            self.label = 'negative'
        elif self.valence == -1:
            self.label = 'n/a'

    def __str__(self):
        return f'TextVAD(Label: {self.label}, Valence: {self.valence}, Arousal: {self.arousal}, Dominance: {self.dominance})'


def analyzefile(input_file, output_dir, mode):
    """
    Performs sentiment analysis on the text file given as input using the NRC-VAD database.
    Outputs results to a new CSV file in output_dir.
    :param input_file: path of .txt file to analyze
    :param output_dir: path of directory to create new output file
    :param mode: determines how sentiment values for a sentence are computed (median or mean)
    :return:
    """
    output_file = os.path.join(output_dir, "Output NRC-VAD Sentiment " +
                               os.path.splitext(os.path.basename(input_file))[0] + ".csv")

    # read file into string
    with open(input_file, 'r') as myfile:
        fulltext = myfile.read()
    # end method if file is empty
    if len(fulltext) < 1:
        print('Empty file.')
        return

    # check each word in sentence for sentiment and write to output_file
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Sentence ID', 'Sentence', 'Sentiment', 'Sentiment Label', 'Arousal', 'Dominance',
                      '# Words Found', 'Found Words', 'All Words']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        analyzetext(fulltext, mode, True,  writer)


def analyzetext(fulltext, mode='mean', split_in_senteces=False, writer=None):
    """
    Performs sentiment analysis on the text given as input using the NRC-VAD database.
    :param fulltext: text to analyze
    :param mode: determines how sentiment values for a sentence are computed (median or mean)
    :param split_in_sentences: determines whether the analysis should split the text in sentences
    :param writer: DictWriter of csv file to which analysis results will be stored
    :return vad: object containing the VAD values of the analyzed text or None
    """
    vad = None
    if split_in_senteces:
        # split into sentences
        sentences = tokenize.sent_tokenize(fulltext)
        vad = []  # list of vad values
    else:
        sentences = [fulltext]

    i = 0  # to store sentence index
    # analyze each sentence for sentiment
    for s in sentences:
        # print("S" + str(i) +": " + s)
        all_words = []
        found_words = []
        v_list = []  # holds valence scores
        a_list = []  # holds arousal scores
        d_list = []  # holds dominance scores

        # search for each valid word's sentiment in NRC-VAD
        words = nlp.pos_tag(s.lower())
        for index, p in enumerate(words):
            # don't process stops or words w/ punctuation
            w = p[0]
            pos = p[1]
            if w in stops or not w.isalpha():
                continue

            # check for negation in 3 words before current word
            j = index-1
            neg = False
            while j >= 0 and j >= index-3:
                if words[j][0] == 'not' or words[j][0] == 'no' or words[j][0] == 'n\'t':
                    neg = True
                    break
                j -= 1

            # lemmatize word based on pos
            if pos[0] == 'N' or pos[0] == 'V':
                lemma = lmtzr.lemmatize(w, pos=pos[0].lower())
            else:
                lemma = w

            all_words.append(lemma)

            # search for lemmatized word in NRC-VAD
            for row in reader:
                if row['Word'].casefold() == lemma.casefold():
                    if neg:
                        found_words.append("neg-"+lemma)
                    else:
                        found_words.append(lemma)
                    v = float(row['Valence'])
                    a = float(row['Arousal'])
                    d = float(row['Dominance'])

                    if neg:
                        # reverse polarity for this word
                        v = .5 - (v - .5)
                        a = .5 - (a - .5)
                        d = .5 - (d - .5)

                    v_list.append(v)
                    a_list.append(a)
                    d_list.append(d)

        if len(found_words) == 0:  # no words found in NRC-VAD for this sentence
            tvad = TextVAD()
            if writer:
                writer.writerow({'Sentence ID': i,
                                 'Sentence': s,
                                 'Sentiment': 'N/A',
                                 'Sentiment Label': 'N/A',
                                 'Arousal': 'N/A',
                                 'Dominance': 'N/A',
                                 '# Words Found': 0,
                                 'Found Words': 'N/A',
                                 'All Words': all_words
                                 })
            i += 1
        else:  # output sentiment info for this sentence

            # get values
            if mode == 'median':
                sentiment = statistics.median(v_list)
                arousal = statistics.median(a_list)
                dominance = statistics.median(d_list)
            else:
                sentiment = statistics.mean(v_list)
                arousal = statistics.mean(a_list)
                dominance = statistics.mean(d_list)

            # set sentiment label
            tvad = TextVAD(sentiment, arousal, dominance)
            if writer:
                writer.writerow({'Sentence ID': i,
                                 'Sentence': s,
                                 'Sentiment': sentiment,
                                 'Sentiment Label': tvad.label,
                                 'Arousal': arousal,
                                 'Dominance': dominance,
                                 '# Words Found': ("%d out of %d" % (len(found_words), len(all_words))),
                                 'Found Words': found_words,
                                 'All Words': all_words
                                 })
            i += 1

        if split_in_senteces:
            vad.append(tvad)
        else:
            vad = tvad

    return vad


def main(input_file, input_dir, output_dir, mode):
    """
    Runs analyzefile on the appropriate files, provided that the input paths are valid.
    :param input_file:
    :param input_dir:
    :param output_dir:
    :param mode:
    :return:
    """

    if len(output_dir) < 0 or not os.path.exists(output_dir):  # empty output
        print('No output directory specified, or path does not exist')
        sys.exit(0)
    elif len(input_file) == 0 and len(input_dir) == 0:  # empty input
        print('No input specified. Please give either a single file or a directory of files to analyze.')
        sys.exit(1)
    elif len(input_file) > 0:  # handle single file
        if os.path.exists(input_file):
            analyzefile(input_file, output_dir, mode)
        else:
            print('Input file "' + input_file + '" is invalid.')
            sys.exit(0)
    elif len(input_dir) > 0:  # handle directory
        if os.path.isdir(input_dir):
            directory = os.fsencode(input_dir)
            for file in os.listdir(directory):
                filename = os.path.join(input_dir, os.fsdecode(file))
                if filename.endswith(".txt"):
                    start_time = time.time()
                    print("Starting sentiment analysis of " + filename + "...")
                    analyzefile(filename, output_dir, mode)
                    print("Finished analyzing " + filename + " in " +
                          str((time.time() - start_time)) + " seconds")
        else:
            print('Input directory "' + input_dir + '" is invalid.')
            sys.exit(0)


if __name__ == '__main__':
    # get arguments from command line
    parser = argparse.ArgumentParser(
        description='Sentiment analysis with NRC-VAD.')
    parser.add_argument('--file', type=str, dest='input_file', default='',
                        help='a string to hold the path of one file to process')
    parser.add_argument('--dir', type=str, dest='input_dir', default='',
                        help='a string to hold the path of a directory of files to process')
    parser.add_argument('--out', type=str, dest='output_dir', default='',
                        help='a string to hold the path of the output directory')
    parser.add_argument('--mode', type=str, dest='mode', default='mean',
                        help='mode with which to calculate sentiment in the sentence: mean or median')
    args = parser.parse_args()

    # run main
    sys.exit(main(args.input_file, args.input_dir, args.output_dir, args.mode))
