"""
Authors:    Doris Zhou, original implementation using NLTK and StanfordNLP
            Javier Wang, adapted to NRC-VAD, extended and optimized with spaCy
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

from nltk.corpus import wordnet as wn
from dataclasses import dataclass, field
from collections import deque
from spacy.tokens import Token, Span, Doc
import spacy
import spacy_fastlang
import _csv
import csv
import sys
import os
import statistics
import time
import argparse

# Suppress fasttext deprecation warning
spacy_fastlang.fasttext.FastText.eprint = lambda x: None

dirname = os.path.dirname(__file__)
# CSV file with lexicon and VAD values
nrc = os.path.join(dirname, "../data/NRC-VAD-Lexicon.csv")
# Use spaCy as Natural Language Processor
nlp = spacy.load('en_core_web_lg')
nlp.select_pipes(disable=['ner', 'parser'])
nlp.add_pipe('language_detector')
nlp.enable_pipe('senter')

# Set language detection attributes for Span objects
Span.set_extension(
    "language", getter=lambda s: s.doc._.language, force=True)
Span.set_extension(
    "language_score", getter=lambda s: s.doc._.language_score, force=True)

# Open NRC-VAD and store as list of dictionaries
with open(nrc, encoding="utf-8-sig") as csvfile:
    reader = list(csv.DictReader(csvfile))

FIELDNAMES = ['Sentence ID', 'Sentence', 'Valence', 'Sentiment Label', 'Sentiment Ratio', 'Arousal', 'Dominance',
              '# Words Found', 'Found Words', 'All Words']

FIELDNAMES_LANG = FIELDNAMES + ['Language', 'Language Score']

NEGATE = ["neither", "never", "none", "nope", "nor", "n\'t", "no", "not",
          "nothing", "nobody", "nowhere", "without", "despite", "rarely",
          "scarcely", "seldom", "hardly"]

INCREASE = \
    ["abnormally", "aboundingly", "absolutely", "absurdly", "abundantly", "accursedly", "admirably",
     "alarmingly", "amazingly", "astronomically", "astoundingly", "awfully", "bally", "best", "bloody",
     "breathtakingly", "clearly", "completely", "considerably", "certainly", "crazy",
     "crazily", "damn", "damned", "darn", "darned", "dead", "decidedly", "deeply", "definitely",
     "doubtlessly", "downright", "dreadfully", "easily", "embarrassingly", "enormously",
     "entirely", "epically", "especially", "everlovingly", "exceedingly", "exceptionally", "excessively",
     "extensively", "extra", "extremely", "fabulously", "fantastically", "far", "fully", "genuinely",
     "greatly", "hella", "highly", "honkingly", "horribly", "hugely", "immensely", "impossibly",
     "incredibly", "indeed", "infinitely", "insanely", "intensely", "largely", "literally", "madly",
     "majorly", "mighty", "more", "most", "much", "noticeably", "observably", "obviously", "outright",
     "particularly", "peculiarly", "perfectly", "positively", "purely", "pretty", "profoundly", "quite",
     "rather", "real", "really", "remarkably", "shockingly", "so", "staggeringly", "strikingly",
     "substantially", "supremely", "surely", "terribly", "thoroughly", "totally", "tremendously", "truly",
     "uberly", "unbelievably", "undeniably", "undoubtedly", "unequivocally", "unimaginably", "unquestionably",
     "unusually", "utterly", "very", "virtually", "way", "whoopingly", "wickedly", "wonderfully"]

INCREASE_EXTRA = \
    ["bleeping", "effing", "flipping", "freaking", "fricking",
        "frigging", "fucking", "motherfreaking", "motherfucking"]

DECREASE = \
    ["almost", "barely", "kinda", "less", "little", "marginally",
     "occasionally", "partly", "slightly", "somewhat", "sorta"]

# Booster multiplers
INC_MUL = 1.25
DEC_MUL = 0.75

# WordNet part-of-speech tags
POS_TAGS = ('N', 'V', 'R', 'J')

# Accepted tags following a modifier
MODIF_POS_TAGS = POS_TAGS + tuple('D')


@dataclass
class VAD:
    """ Class containing VAD data """

    valence:   float
    arousal:   float
    dominance: float
    label:     str = field(init=False)

    def __post_init__(self):
        # Set sentiment label
        self.label = self.sentiment_label(self.valence)

    @staticmethod
    def sentiment_label(valence: float):
        """ Assigns a valence-based sentiment label """
        if valence > .55:
            return 'positive'
        elif valence < .45:
            return 'negative'
        else:
            return 'neutral'

    def __str__(self):
        return f'VAD(Label: {self.label}, V: {self.valence}, A: {self.arousal}, D: {self.dominance})'

    def __iter__(self):
        return iter([self.label, self.valence, self.arousal, self.dominance])


def analyze_file(input_file: str,
                 output_dir: str,
                 mode:       str,
                 lang_check: bool = False) -> None:
    """ Performs sentiment analysis on the text file given as input using the NRC-VAD lexicon.
    Outputs results to a new CSV file in `output_dir`.

    Args:
        input_file (str): Path of text file to analyze
        output_dir (str): Path of directory to create new output file
        mode (str): Determines how sentiment values for a sentence are computed (median or mean)
        lang_check (bool): Whether to include language information in the analysis

    Returns:
        None
    """
    output_file = os.path.join(output_dir, "Output NRC-VAD Sentiment " +
                               os.path.splitext(os.path.basename(input_file))[0] + ".csv")

    # Read file into string
    with open(input_file, 'r') as myfile:
        fulltext = myfile.read()
    # End method if file is empty
    if len(fulltext) < 1:
        print('Empty file.')
        return

    # Check each word in sentence for sentiment and write to output_file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if lang_check:
            fields = FIELDNAMES_LANG
        else:
            fields = FIELDNAMES
        writer.writerow(fields)  # Write header

        analyze_text(fulltext, mode, True, lang_check, writer)


def analyze_text(fulltext:   str,
                 mode:       str = 'mean',
                 detailed:   bool = False,
                 lang_check: bool = False,
                 writer:     '_csv._writer' = None) -> list[VAD | list]:
    """ Performs sentiment analysis on the sentences of a text using the NRC-VAD lexicon.

    Args:
        fulltext (str): Text to split into sentences and analyze
        mode (str): Determines how sentiment values for a sentence are computed (median or mean)
        detailed (bool): Determines whether the detailed values of the analysis should be returned
        lang_check (bool): Whether to include language information in the detailed analysis
        writer (_csv._writer): Writer of CSV file in which analysis results will be stored

    Returns:
        list[VAD | list]: `VAD` objects with values from the analyzed text;
            or lists of values that map to fieldnames, but without an index
    """
    # Split into sentences
    sentences = nlp(fulltext).sents
    vad = []  # List of vad analysis values

    # Analyze each sentence for sentiment
    for i, s in enumerate(sentences):
        values = analyze_parsed_string(s, mode, detailed, lang_check)
        if detailed:
            # Append sentence index
            values.appendleft(i)

        # Output sentiment info for this sentence
        if writer:
            writer.writerow(values)

        vad.append(values)

    return vad


def analyze_string(string:     str,
                   mode:       str = 'mean',
                   detailed:   bool = False,
                   lang_check: bool = False) -> VAD | list:
    """ Performs sentiment analysis on a string using the NRC-VAD lexicon.

    Args:
        string (str): String to be analyzed
        mode (str): Determines how sentiment values are computed (median or mean)
        detailed (bool): Determines whether the detailed values of the analysis should be returned
        lang_check (bool): Whether to include language information in the detailed analysis

    Returns:
        VAD | list: `VAD` object containing the VAD values of the string, None if no words were analyzed;
            or list of values that map to fieldnames, but without an index
    """
    return analyze_parsed_string(nlp(string), mode, detailed, lang_check)


def analyze_parsed_string(parsed_str: Doc | Span,
                          mode:       str = 'mean',
                          detailed:   bool = False,
                          lang_check: bool = False) -> VAD | list:
    """ Performs sentiment analysis on a `Doc`/`Span` object from a parsed string
    using the NRC-VAD lexicon.

    Args:
        parsed_str (Doc | Span): Sequence of tokens from a string parsed with spaCy NLP
        mode (str): Determines how sentiment values are computed (median or mean)
        detailed (bool): Determines whether the detailed values of the analysis should be returned
        lang_check (bool): Whether to include language information in the detailed analysis

    Returns:
        VAD | list: `VAD` object containing the VAD values of the string, None if no words were analyzed;
            or list of values that map to fieldnames, but without an index
    """
    all_words = []
    found_words = []
    v_list = []  # Holds valence scores
    a_list = []  # Holds arousal scores
    d_list = []  # Holds dominance scores
    pos_words = neg_words = 0  # Counts words for each label

    # Input Doc/Span object and raw string
    words = parsed_str
    text = parsed_str.text

    # Search for each valid word's sentiment in NRC-VAD
    for index, token in enumerate(words):
        # Get POS fine-grained tag
        pos = token.tag_[0]

        # Don't process stops or words w/ punctuation
        if (token.is_stop and pos != 'N') or not token.is_alpha:
            continue

        # Search for lemmatized word in NRC-VAD
        # and evaluate its VAD values
        lemma, results = search_and_evaluate(
            token, pos, index, words)

        all_words.append(lemma)

        # Word was found
        if results:
            # Prefixed string, VAD values and whether sentiment is positive
            append_str, v, a, d, positive = results

            found_words.append(append_str)
            v_list.append(v)
            a_list.append(a)
            d_list.append(d)

            if positive:
                pos_words += 1
            elif positive is False:
                neg_words += 1

    num_found = len(found_words)
    if num_found == 0:  # No words found in NRC-VAD for this sentence
        if detailed:
            vad = deque([text, 'N/A', 'N/A', 'N/A', 'N/A',
                        'N/A', 0, 'N/A', all_words])
        else:
            vad = None

    else:
        # Get VAD values
        if mode == 'median':
            sentiment = max(min(1, statistics.median(v_list)), 0)
            arousal = statistics.median(a_list)
            dominance = statistics.median(d_list)
        else:
            sentiment = max(min(1, statistics.fmean(v_list)), 0)
            arousal = statistics.fmean(a_list)
            dominance = statistics.fmean(d_list)

        # Set sentiment label
        vad = VAD(sentiment, arousal, dominance)
        if detailed:
            # Sentiment ratio score
            sratio = (pos_words - neg_words) / max(1, pos_words + neg_words)
            vad = deque([text, sentiment, vad.label, sratio, arousal, dominance, ("%d out of %d" % (
                num_found, len(all_words))), found_words, all_words])

    # Language detection attributes
    if detailed and lang_check:
        lang, lang_score = parsed_str._.language, parsed_str._.language_score
        vad.extend([lang, lang_score])

    return vad


def search_and_evaluate(token:         Token,
                        pos:           str,
                        current_index: int,
                        words:         Doc | Span) -> tuple:
    """ Searches for the current word in NRC-VAD lexicon while
    analyzing modifiers and obtaining its VAD values.

    Args:
        token (Token): Token containing current lemma
        pos (str): Unprocessed word's part-of-speech tag
        current_index (int): Index of current token/word
        words (Doc | Span): Sequence of tokens from current analysis

    Returns: 
        tuple: Token's lemma, prefixed string, VAD values and whether sentiment is positive; 
            or token's lemma and None, if the search failed
    """
    # -------------- AUXILIARY FUNCTIONS --------------

    def _lemmatize_by_pos(token: Token, pos: str) -> tuple:
        """ Lemmatizes word depending on tag in `POS_TAGS` 
        and adapts tag to WordNet if necessary.

        Args:
            token (Token): Token containing lemma
            pos (str): Unprocessed word's part-of-speech tag

        Returns:
            tuple: Lemma and WordNet's POS tag
        """
        lemma = token.lower_
        if pos in POS_TAGS:
            if pos == 'N' or pos == 'V':
                lemma = token.lemma_.lower()

            # Adapt to WordNet ADJ pos
            elif pos == 'J':
                pos = 'A'
        else:
            pos = None
        return lemma, pos

    def _check_modifiers(current_index: int, words: Doc | Span) -> tuple:
        """ Checks for sentiment modifiers in three words before
        the current one. Skips non-alphanumerics and adverbs.

        Args:
            current_index (int): Index of current token/word
            words (Doc | Span): Sequence of tokens from current analysis

        Returns:
            tuple: Modifier flags (`neg`, `first_neg` and `inc`)
        """
        neg = inc = None
        first_neg = False

        j = current_index - 1
        while j >= 0 and j >= current_index - 3:
            prior_tok = words[j]
            if neg is None and prior_tok.lower_ in NEGATE:
                neg = True
                first_neg = inc is not None

            is_adverb = prior_tok.tag_[0] == 'R'
            is_other_boost = prior_tok.tag_ in (
                'UH', 'VBG', 'VBP')
            # Check next word POS (only for adverbs)
            if inc is None and (is_other_boost or words[j + 1].tag_[0] in MODIF_POS_TAGS):
                if is_adverb:
                    if prior_tok.lower_ in INCREASE:
                        inc = True
                    elif prior_tok.lower_ in DECREASE:
                        inc = False
                elif is_other_boost and prior_tok.lower_ in INCREASE_EXTRA:
                    inc = True

            # Stop at start of current sentence or if both modifiers are active
            if prior_tok.is_sent_start or (neg is not None and inc is not None):
                break

            # Do not count adverbs or non-alphanumerics
            if is_adverb or not prior_tok.is_alpha:
                current_index -= 1
            j -= 1

        if first_neg:
            # Neg before modifier
            neg = False
            inc = not inc  # Reverse booster polarity

        return neg, first_neg, inc

    def _append_prefix_modifiers(orig_lemma: str,
                                 syn_lemma:  str | None,
                                 neg:        bool,
                                 first_neg:  bool,
                                 inc:        bool) -> str:
        """ Constructs a string with the original lemma and indicators
        of all modifiers, including synonym lemma, as prefixes.

        Args:
            orig_lemma (str): Original lemma (not a synonym)
            syn_lemma (str | None): Synonym of original lemma if found, else None
            neg (bool): Whether the sentiment was negated
            first_neg (bool): Whether the negating word came first
            inc (bool): Whether the sentiment was increased or decreased

        Returns:
            str: Prefixed string
        """
        append_str = orig_lemma
        if inc is not None:
            if inc:
                append_str = "inc-" + append_str
            else:
                append_str = "dec-" + append_str

        if neg and not first_neg:
            append_str = "neg-" + append_str

        if syn_lemma:
            append_str = "syn(" + syn_lemma + ")-" + append_str

        return append_str

    def _apply_modifiers(v:   float,
                         a:   float,
                         d:   float,
                         neg: bool,
                         inc: bool) -> tuple:
        """ Applies modifiers obtained in `_check_modifiers`
        to the original VAD values.

        Args:
            v (float): Original valence
            a (float): Original arousal
            d (float): Original dominance
            neg (bool): Whether the sentiment was negated
            inc (bool): Whether the sentiment was increased or decreased

        Returns:
            tuple: Modified VAD values and whether sentiment is positive
        """
        if neg:
            # Reverse polarity for this word
            v = 1 - v
            a = 1 - a
            d = 1 - d

        l = VAD.sentiment_label(v)

        positive = None

        # Apply modifiers
        if l[0] == 'p':  # Positive
            positive = True

            if inc is True:
                v *= INC_MUL  # Increase positive valence
            if inc is False:
                v *= DEC_MUL  # Decrease positive valence

        elif l[2] == 'g':  # Negative
            positive = False

            if inc is True:
                v = 1 - INC_MUL*(1-v)  # Decrease negative valence
            if inc is False:
                v = 1 - DEC_MUL*(1-v)  # Increase negative valence

        return v, a, d, positive

    def _get_synonyms(orig_lemma: str, wn_pos: str) -> list | None:
        """ Obtains synonyms for a lemma keeping its part of speech.

        Args:
            orig_lemma (str): Lemma to search synonyms for
            wn_pos (str): WordNet's POS tag for current word

        Returns: 
            list | None: Synonyms or None if not found
        """
        syns = dict()

        # Look for synonyms in synsets
        for syn in wn.synsets(lemma, pos=wn_pos.lower()):
            for l in syn.lemmas():
                name = l.name()
                # Avoid compounds
                if '_' not in name:
                    syns[name] = None

        if syns:
            # Remove original lemma if present
            syns.pop(orig_lemma, None)
            return list(syns.keys())
        else:
            return None

    # -------------- END AUXILIARY FUNCTIONS --------------

    # Lemmatize word using part-of-speech
    lemma, wn_pos = _lemmatize_by_pos(token, pos)

    syns = []  # Holds synonyms
    s = 0  # Synonyms index
    orig_lemma = lemma  # Original lemma

    # Search until found or break
    while True:
        if syns:
            # Search for next synonym
            lemma = syns[s]
            s += 1

        # Search word in NRC-VAD
        for row in reader:
            if row['Word'].casefold() == lemma.casefold():

                # Check for negation and degree adverbs in 3 words before current word
                if token.is_sent_start:
                    neg = None  # Negation
                    first_neg = False  # Negation detected first
                    inc = None  # Increase or Decrease
                else:
                    neg, first_neg, inc = _check_modifiers(
                        current_index, words)

                append_str = _append_prefix_modifiers(
                    orig_lemma, lemma if syns else None, neg, first_neg, inc)

                v = float(row['Valence'])
                a = float(row['Arousal'])
                d = float(row['Dominance'])

                results = (append_str,) + _apply_modifiers(v, a, d, neg, inc)
                return orig_lemma, results

        # POS not suitable for synonyms
        if not wn_pos:
            break

        # Lemma not found in NRC-VAD, check for synonyms
        if not syns:
            syns = _get_synonyms(orig_lemma, wn_pos)

            # No synonyms found
            if not syns:
                break

        if s == len(syns):
            break

    return orig_lemma, None


def main(input_file: str, input_dir: str, output_dir: str, mode: str) -> None:
    """ Runs `analyze_file` on the appropriate files, saving analysis results
    in the corresponding CSV files at `output_dir`.

    Args:
        input_file (str): File to be analyzed
        input_dir (str): Directory that contains `input_file`
        output_dir (str): Directory to store analysis results
        mode (str): Sentiment computation mode (mean or median)

    Returns:
        None
    """
    if len(output_dir) < 0 or not os.path.exists(output_dir):  # Empty output
        print('No output directory specified, or path does not exist')
        sys.exit(0)
    elif len(input_file) == 0 and len(input_dir) == 0:  # Empty input
        print('No input specified. Please give either a single file or a directory of files to analyze.')
        sys.exit(1)
    elif len(input_file) > 0:  # Handle single file
        if os.path.exists(input_file):
            analyze_file(input_file, output_dir, mode)
        else:
            print('Input file "' + input_file + '" is invalid.')
            sys.exit(0)
    elif len(input_dir) > 0:  # Handle directory
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
    # Get arguments from command line
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

    # Run main
    sys.exit(main(args.input_file, args.input_dir, args.output_dir, args.mode))
