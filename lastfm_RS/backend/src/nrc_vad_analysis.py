"""
Author: Doris Zhou
    Adapted to NRC-VAD and optimized with spaCy by Javier Wang
Date: August 6, 2022
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

from nltk.corpus import wordnet as wn
from dataclasses import dataclass, field
from collections import deque
import spacy
import csv
import sys
import os
import statistics
import time
import argparse

dirname = os.path.dirname(__file__)
# CSV file with lexicon and VAD values
nrc = os.path.join(dirname, "../data/NRC-VAD-Lexicon.csv")
# Use spaCy as Natural Language Processor
nlp = spacy.load('en_core_web_lg', disable=['parser', 'ner'])
nlp.enable_pipe('senter')

# Open NRC-VAD and store as list of dictionaries
with open(nrc, encoding="utf-8-sig") as csvfile:
    reader = list(csv.DictReader(csvfile))

FIELDNAMES = ['Sentence ID', 'Sentence', 'Valence', 'Sentiment Label', 'Sentiment Score', 'Arousal', 'Dominance',
              '# Words Found', 'Found Words', 'All Words']

NEGATE = ["neither", "never", "none", "nope", "nor", "n\'t", "no", "not",
          "nothing", "nobody", "nowhere", "without", "despite", "rarely",
          "scarcely", "seldom", "hardly"]

INCREASE = \
    ["abnormally", "aboundingly", "absolutely", "absurdly", "abundantly", "accursedly", "admirably",
     "alarmingly", "amazingly", "astronomically", "astoundingly", "awfully", "bally", "bloody",
     "bleeping", "breathtakingly", "clearly", "completely", "considerably", "certainly", "crazy",
     "crazily", "damn", "damned", "darn", "darned", "dead", "decidedly", "deeply", "definitely",
     "doubtlessly", "downright", "dreadfully", "easily", "effing", "embarrassingly", "enormously",
     "entirely", "epically", "especially", "everloving", "exceedingly", "exceptionally", "excessively",
     "extensively", "extra", "extremely", "fabulously", "fantastically", "far", "flipping", "freaking",
     "fricking", "frigging", "fucking", "fully", "genuinely", "greatly", "hella", "highly", "honkingly",
     "horribly", "hugely", "immensely", "impossibly", "incredibly", "indeed", "infinitely", "insanely",
     "intensely", "largely", "literally", "madly", "majorly", "mighty", "more", "most", "motherfreaking",
     "motherfucking", "much", "noticeably", "observably", "obviously", "outright", "particularly",
     "peculiarly", "perfectly", "positively", "purely", "pretty", "profoundly", "quite", "rather", "real",
     "really", "remarkably", "shockingly", "so", "staggeringly", "strikingly", "substantially",
     "supremely", "surely", "terribly", "thoroughly", "totally", "tremendously", "truly", "uberly",
     "unbelievably", "undeniably", "undoubtedly", "unequivocally", "unimaginably", "unquestionably",
     "unusually", "utterly", "very", "virtually", "way", "whoopingly", "wickedly", "wonderfully"]

DECREASE = \
    ["almost", "barely", "kinda", "less", "little", "marginally",
     "occasionally", "partly", "slightly", "somewhat", "sorta"]


@dataclass
class VAD:
    """
    Class containing data for VAD values
    """
    valence: float
    arousal: float
    dominance: float
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

    def __str__(self):
        return f'VAD(Label: {self.label}, V: {self.valence}, A: {self.arousal}, D: {self.dominance})'

    def __iter__(self):
        return iter([self.label, self.valence, self.arousal, self.dominance])


def analyze_file(input_file, output_dir, mode):
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
        writer = csv.writer(csvfile)
        writer.writerow(FIELDNAMES)  # write header

        analyze_text(fulltext, mode, True, writer)


def analyze_text(fulltext, mode, detailed=False, writer=None):
    """
    Performs sentiment analysis on the sentences of a text using the NRC-VAD database.
    :param fulltext: string of the text to split into sentences and analyze
    :param mode: determines how sentiment values for a sentence are computed (median or mean)
    :param detailed: determines whether the detailed values of the analysis should be returned
    :param writer: csv.writer of csv file to which analysis results will be stored
    :return either:
        - list of objects with VAD values of the analyzed text
        - list of lists of values that map to fieldnames, but without an index
    """

    # split into sentences
    sentences = nlp(fulltext).sents
    vad = []  # list of vad analysis values

    # analyze each sentence for sentiment
    for i, s in enumerate(sentences):
        values = analyze_parsed_string(s, mode, detailed)
        if detailed:
            # append sentence index
            values.appendleft(i)

        # output sentiment info for this sentence
        if writer:
            writer.writerow(values)

        vad.append(values)

    return vad


def analyze_string(string, mode, detailed=False):
    """
    Performs sentiment analysis on a string using the NRC-VAD database.
    :param string: string to be analyzed
    :param mode: determines how sentiment values are computed (median or mean)
    :param detailed: determines whether the detailed values of the analysis should be returned
    :return either:
        - VAD object containing the VAD values of the string; or None if no words were analyzed
        - list of values that map to fieldnames, but without an index
    """
    return analyze_parsed_string(nlp(string), mode, detailed)


def analyze_parsed_string(parsed_str, mode='mean', detailed=False):
    """
    Performs sentiment analysis on a Doc/Span object from a parsed string using
    the NRC-VAD database.
    :param parsed_str: Doc/Span object from a string parsed with spaCy NLP
    :param mode: determines how sentiment values are computed (median or mean)
    :param detailed: determines whether the detailed values of the analysis should be returned
    :return either:
        - VAD object containing the VAD values of the string; or None if no words were analyzed
        - list of values that map to fieldnames, but without an index
    """

    all_words = []
    found_words = []
    v_list = []  # holds valence scores
    a_list = []  # holds arousal scores
    d_list = []  # holds dominance scores
    pos_words = neg_words = 0  # counts words for each label

    # input Doc/Span object and raw string
    words = parsed_str
    text = parsed_str.text

    # search for each valid word's sentiment in NRC-VAD
    for index, token in enumerate(words):
        w = token.lower_
        # get pos fine-grained tag
        pos = token.tag_[0]

        # don't process stops or words w/ punctuation
        if (token.is_stop and pos != 'N') or not token.is_alpha:
            continue

        # lemmatize word based on part-of-speech
        lemma = w
        pos_tags = ('N', 'V', 'R', 'J')
        if pos in pos_tags:
            if pos == 'N' or pos == 'V':
                lemma = token.lemma_.lower()

            # adapt to wordnet ADJ pos
            elif pos == 'J':
                pos = 'A'
        else:
            pos = None

        all_words.append(lemma)

        # search for lemmatized word in NRC-VAD
        found = False
        syns = []  # holds synonyms
        s = 0  # synonyms index
        orig_lemma = lemma  # original lemma
        # accepted tags following a modifier
        modif_pos_tags = pos_tags + tuple('D')
        while not found:
            if syns:
                # search for next synonym
                lemma = syns[s]
                s += 1

            for row in reader:
                if row['Word'].casefold() == lemma.casefold():

                    # check for negation and degree adverbs in 3 words before current word
                    neg = None  # negation
                    first_neg = False  # negation detected first
                    inc = None  # increase or decrease
                    if not token.is_sent_start:
                        j = index - 1
                        while j >= 0 and j >= index - 3:
                            prior_tok = words[j]
                            if neg is None and prior_tok.lower_ in NEGATE:
                                neg = True
                                first_neg = inc is not None

                            is_adverb = prior_tok.tag_[0] == 'R'
                            if inc is None and is_adverb and words[j + 1].tag_[0] in modif_pos_tags:
                                if prior_tok.lower_ in INCREASE:
                                    inc = True
                                elif prior_tok.lower_ in DECREASE:
                                    inc = False

                            # stop at start of current sentence or if both modifiers are active
                            if prior_tok.is_sent_start or (neg is not None and inc is not None):
                                break

                            # do not count adverbs or non-alphanumerics
                            if is_adverb or not prior_tok.is_alpha:
                                index -= 1
                            j -= 1

                    append_str = orig_lemma
                    if inc is not None:
                        # neg before modifier
                        if first_neg:
                            neg = False
                            inc = not inc  # reverse booster polarity

                        if inc:
                            append_str = "inc-" + append_str
                        else:
                            append_str = "dec-" + append_str

                    if neg and not first_neg:
                        append_str = "neg-" + append_str

                    if syns:
                        append_str = "syn(" + lemma + ")-" + append_str

                    found_words.append(append_str)

                    v = float(row['Valence'])
                    a = float(row['Arousal'])
                    d = float(row['Dominance'])

                    if neg:
                        # reverse polarity for this word
                        v = 1 - v
                        a = 1 - a
                        d = 1 - d

                    l = VAD(v, a, d).label

                    # apply modifiers
                    if l[0] == 'p':  # positive
                        pos_words += 1

                        if inc is True:
                            v *= 1.25  # increase positive valence
                        if inc is False:
                            v *= 0.75  # decrease positive valence

                    elif l[2] == 'g':  # negative
                        neg_words += 1

                        if inc is True:
                            v = 1 - 1.25*(1-v)  # decrease negative valence
                        if inc is False:
                            v = 1 - 0.75*(1-v)  # increase negative valence

                    v_list.append(v)
                    a_list.append(a)
                    d_list.append(d)

                    found = True
                    break

            # pos not suitable for synonyms
            if not pos:
                break

            # lemma not found in nrc-vad
            if not found:
                # check for synonyms
                if not syns:
                    syns = dict()
                    # look for synonyms in synsets
                    for syn in wn.synsets(lemma, pos=pos.lower()):
                        for l in syn.lemmas():
                            name = l.name()
                            # avoid compounds
                            if '_' not in name:
                                syns[name] = None

                    # no synonyms found
                    if not syns:
                        break

                    # remove original lemma if present
                    if syns.get(orig_lemma):
                        del syns[orig_lemma]
                    syns = list(syns.keys())

                if s == len(syns):
                    break

    if len(found_words) == 0:  # no words found in NRC-VAD for this sentence
        if detailed:
            vad = deque([text, 'N/A', 'N/A', 'N/A'
                        'N/A', 'N/A', 0, 'N/A', all_words])
        else:
            vad = None

    else:
        # get vad values
        if mode == 'median':
            sentiment = max(min(1, statistics.median(v_list)), 0)
            arousal = statistics.median(a_list)
            dominance = statistics.median(d_list)
        else:
            sentiment = max(min(1, statistics.fmean(v_list)), 0)
            arousal = statistics.fmean(a_list)
            dominance = statistics.fmean(d_list)

        # set sentiment label
        vad = VAD(sentiment, arousal, dominance)
        if detailed:
            num_found = len(found_words)
            stsc = (pos_words - neg_words) / num_found
            vad = deque([text, sentiment, vad.label, stsc, arousal, dominance, ("%d out of %d" % (
                num_found, len(all_words))), found_words, all_words])

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
            analyze_file(input_file, output_dir, mode)
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
                    analyze_file(filename, output_dir, mode)
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
