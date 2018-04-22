import nltk
import re
import os

from nltk.tokenize import word_tokenize
from nltk.corpus import brown
from nltk.tokenize import sent_tokenize
from nltk.corpus import wordnet as wn
from nltk import pos_tag
from nltk.parse.stanford import StanfordParser
from nltk.stem import WordNetLemmatizer
#from nltk.corpus import treebank


class EssayGrader:

    rules = {"NP VP": "S", "V PN": "VP", 'Det Nominal': 'NP',   'Nominal PP': 'Nominal', 'Adj Nominal': 'Nominal', 'Prep NP': 'PP'}
    terminal = {'NN': 'NP', 'PN': "NP"}
    verb_tags = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]  # all the verb tages
    subject_tags_P = ['NNS', 'NNPS']
    subject_tags_S = ['NN', 'NNP']
    PRP_words = ['you', 'You', 'we', 'We', 'they', 'They', 'I', 'i']
    wrong_verb_combo = ['TO VBD', 'TO VBG', 'TO VBN', 'TO VBZ', 'MD VBD', 'MD VBG', 'MD VBN', 'MD VBZ', 'VBZ VB', 'VBZ VBD', 'VBZ VBP', 'VBZ VBZ', 'VBP VB', 'VBP VBD', 'VBP VBP', 'VBP VBZ']
    wrong_sub_v_combo = ['NN VB', 'NN VBP', 'NNS VBZ', 'NNP VB', 'NNP VBP', 'NNPS VBZ','PRPP VBZ', 'PRPS VB', 'PRPS VBP']

    # file name and information
    filename = None
    essay_text = None
    sentences_of_essay = None

    # result stream writer
    result_writer = None

    # sub score values
    essay_length_score = None
    spelling_mistake_score = None
    subject_verb_agreement_score = None
    verb_score = None
    sentence_formation_score = None
    essay_coherent_score = None
    essay_answer_score = None

    # final score and classifier
    final_score = None
    final_grade = None

    # internal values needed between methods
    word_count = None
    verb_count = None
    sentence_count = None
    subject_verb_disagreement_count = None
    missing_verb_count = None
    verb_tense_disagreement_or_misuse = None
    fragment_count = None

    # class constructor
    def __init__(self, filename_path, filename, result_writer):
        self.filename = filename
        self.result_writer = result_writer
        self.essay_text = self.retrieve_essay_text(filename_path)

    def retrieve_essay_text(self, filename_path):
        text_stream = open(filename_path, 'r')
        text = text_stream.read()
        text_stream.close()
        return text

    def prepare_data(self):
        # split text by sentences and get sentence count
        self.sentences_of_essay = sent_tokenize(self.essay_text)
        self.sentence_count = len(self.sentences_of_essay)

        # get total words by removing characters that are not alpha-numeric and making contractions count as one word
        total_words = word_tokenize(re.sub('[^a-zA-Z0-9\s]', '', self.essay_text))
        self.word_count = len(total_words)

        # get verb count
        sent_tokens = [word_tokenize(sentence) for sentence in self.sentences_of_essay]
        tagged_sent_tokens = [pos_tag(sentence) for sentence in sent_tokens]
        verb_list = [word[0] for sentence in tagged_sent_tokens for word in sentence if word[1] in self.verb_tags]
        self.verb_count = len(verb_list)

        # get subject verb mismatch count ie plural singular
        self.subject_verb_disagreement_count = self.get_subject_verb_disagreement(tagged_sent_tokens)

        # get missing verb count
        self.missing_verb_count = self.get_missing_verb(tagged_sent_tokens)

        # get verb tense disagreement count, and/or misuse of verb count
        self.verb_tense_disagreement_or_misuse = self.get_verb_tense_disagreement_or_misuse(tagged_sent_tokens)

        #get fragment count
        self.fragment_count = self.count_fragments()

    def get_subject_verb_disagreement(self, tagged_sent_tokens):

        disagreement_count = 0
        word_index = 0
        tag_index = 1

        for sentence in tagged_sent_tokens:

            sentence_length = len(sentence)

            for index in range(0, sentence_length - 1):

                tag_combo = ""

                # check if tag is personal pronoun
                if sentence[index][tag_index] == "PRP":

                    # check if personal pronoun is singular
                    if sentence[index][word_index] in self.PRP_words:
                        tag_combo = "PRPP" + " " + sentence[index + 1][tag_index]
                    # if not singular do this
                    else:
                        tag_combo = "PRPS" + " " + sentence[index + 1][tag_index]
                else:
                    tag_combo = sentence[index + 1][tag_index] + " " + sentence[index + 1][tag_index]

                if tag_combo in self.wrong_sub_v_combo:
                    disagreement_count += 1

        return disagreement_count

    def get_missing_verb(self, tagged_sent_tokens):

        missing_count = 0
        tag_index = 1

        for sentence in tagged_sent_tokens:
            # reset count
            sentence_verb_count = 0
            # count verbs in this loop
            for word in sentence:
                if word[tag_index] in self.verb_tags:
                    sentence_verb_count += 1
            # if no verbs in sentences add to missing count
            if sentence_verb_count == 0:
                missing_count += 1

        return missing_count

    def get_verb_tense_disagreement_or_misuse(self, tagged_sent_tokens):

        tag_index = 1
        disagreement_misuse_count = 0

        for sentence in tagged_sent_tokens:

            sentence_length = len(sentence)

            for index in range(sentence_length - 1):
                tag_combo = sentence[index][tag_index] + ' ' + sentence[index + 1][tag_index]
                if tag_combo in self.wrong_verb_combo:
                    disagreement_misuse_count += 1

        return disagreement_misuse_count

    def count_fragments(self):

        frag_count = 0

        for sentence in self.sentences_of_essay:
            tree_data_iterator = self.parse_tree(sentence)
            tree_data = next(tree_data_iterator)
            frag = 0
            if 'FRAG' == tree_data[frag].label():
                frag_count += 1
        print('fragmented sentences: ', str(frag_count))
        return frag_count

    def parse_tree(self, text):
        os.environ['STANFORD_PARSER']=os.getcwd() + "/stanford-parser-full-2018-02-27"
        os.environ['STANFORD_MODELS']=os.getcwd() + "/stanford-parser-full-2018-02-27"

        stanford_parser = StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
        result = stanford_parser.raw_parse(text)
        return result

    def determine_sub_and_final_scores(self):
        # get sub-scores
        self.essay_length_score = self.compute_essay_length_score()
        self.spelling_mistake_score = self.compute_spelling_mistake_score()
        self.subject_verb_agreement_score = self.compute_subject_verb_agreement_score()
        self.verb_score = self.compute_verb_score()
        self.sentence_formation_score = self.compute_sentence_formation_score()
        self.essay_coherent_score = self.compute_essay_coherent_score()
        self.essay_answer_score = 0

        # get final score after computing sub-scores
        self.final_score = self.compute_final_score()

    def compute_essay_length_score(self):
        modified_length = int((self.verb_count/3) + (self.sentence_count/2))
        if modified_length <= 11:
            return 1
        elif modified_length <= 14:
            return 2
        elif modified_length <= 16:
            return 3
        elif modified_length <= 18:
            return 4
        else:
            return 5

    def compute_spelling_mistake_score(self):
        total_words = word_tokenize(re.sub('[^a-zA-Z0-9\s]', '', self.essay_text))
        bad_spelling_count = 0
        dictionary = set(brown.words())

        for word in total_words:
            if word not in dictionary and word != 'n\'t':
                bad_spelling_count += 1

        # high spelling ratio == almost no mistakes : low spelling ration == mistakes
        spelling_ratio = int(self.word_count / (bad_spelling_count + 0.0001))
        if spelling_ratio >= 30:
            return 0
        elif spelling_ratio >= 24:
            return 1
        elif spelling_ratio >= 20:
            return 2
        elif spelling_ratio >= 16:
            return 3
        else:
            return 4

    def compute_subject_verb_agreement_score(self):

        verb_ratio = int(self.verb_count / (self.subject_verb_disagreement_count + 0.0001))

        if verb_ratio <= 16:
            return self._helper_compute_verb_score(1)
        elif verb_ratio <= 26:
            return self._helper_compute_verb_score(2)
        elif verb_ratio <= 35:
            return self._helper_compute_verb_score(3)
        elif verb_ratio <= 44:
            return self._helper_compute_verb_score(4)
        else:
            return self._helper_compute_verb_score(5)

    def _helper_compute_verb_score(self, value):

        new_value = int(value * (self.word_count / 280) * (self.verb_count/45))
        if new_value > 5:
            return 5
        return new_value

    def compute_verb_score(self):

        denominator = self.missing_verb_count + self.verb_tense_disagreement_or_misuse

        if denominator == 0:
            missing_verb_ratio = 1000
        else:
            missing_verb_ratio = self.verb_count / denominator

        if missing_verb_ratio <= 14:
            return self._helper_compute_verb_score(1)
        elif missing_verb_ratio <= 50:
            return self._helper_compute_verb_score(2)
        elif missing_verb_ratio <= 85:
            return self._helper_compute_verb_score(3)
        elif missing_verb_ratio <= 110:
            return self._helper_compute_verb_score(4)
        else:
            return self._helper_compute_verb_score(5)

    def compute_sentence_formation_score(self):
        # manipulate self.fragment_count here
        return 0

    def compute_essay_coherent_score(self):
        #get pronouns remove anything that isnt third person
        return 0

    def compute_final_score(self):
        a = self.essay_length_score
        b = self.spelling_mistake_score
        ci = self.subject_verb_agreement_score
        cii = self.verb_score
        ciii = self.sentence_formation_score
        di = self.essay_coherent_score
        dii = self.essay_answer_score

        # formula given by project part 1
        # TODO verify its the same for part 2
        return (2 * a) - b + ci + cii + (2 * ciii) + (2 * di) + (3 * dii)

    def determine_classifier(self):
        if self.sentence_count < 10:
            self.final_grade = 'LOW'
        elif self.final_score >= 12:
            self.final_grade = 'HIGH'
        else:
            self.final_grade = 'LOW'

    def write(self):
        self.result_writer.write(self.filename + ';' + str(self.essay_length_score) + ';' + str(self.spelling_mistake_score) + ';' + str(self.subject_verb_agreement_score) + ';' + str(self.verb_score) + ';' + str(self.sentence_formation_score) + ';' + str(self.essay_coherent_score) + ';' + str(self.essay_answer_score) + ';' + str(self.final_score) + ';' + self.final_grade + '\n')
