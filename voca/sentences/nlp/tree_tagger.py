import operator
import re
from .treetaggerwrapper import TreeTagger, make_tags
from .pos_patterns import pos_patterns

PROBA_THRESHOLD = 0.1


class VocaTagger:
    def __init__(self, lang):
        self.tagger = TreeTagger(TAGLANG=lang)
        self.pos_patterns = pos_patterns[lang]
        self.probabilities = None
        self.lang = lang

    def tag_word(self, word, search_group=None, initial=False):
        tag = make_tags(self.tagger.tag_text(word), allow_extra=True)[0]
        return self.__most_likely_tag(tag.extra, search_group, initial)

    def word_tag_info(self, word, search_group, initial):
        pos = self.tag_word(word, search_group, initial)
        for description, cat, pattern in self.pos_patterns:
            if re.match(pattern, pos):
                return description, cat, pos
        return "Unknown type", "unk", None

    def is_noun(self, word, use_proba=True):
        pos = self.tag_word(word)
        return self.pos_is_noun(pos)

    def is_verb(self, word):
        pos = self.tag_word(word)
        return self.pos_is_verb(pos)

    def is_adjective(self, word):
        pos = self.tag_word(word)
        return self.pos_is_adj(pos)

    def pos_is_noun(self, pos):
        if self.lang in ["de", "es", "fr", "it", "en"]:
            return pos[0] == "N"
        elif self.lang == "nl":
            return pos[0:4] == "noun"

    def pos_is_verb(self, pos):
        if self.lang in ["de", "es", "fr", "it"]:
            return pos[0] == "V"
        elif self.lang == "en":
            return pos[0] == "V" or pos == "MD"
        elif self.lang == "nl":
            return pos[0] == "v"
        return False

    def pos_is_adj(self, pos):
        if self.lang == "en":
            return pos[0:2] == "JJ"
        else:
            return pos[0:3].lower() == "adj"
        return False

    def __most_likely_tag(self, tups, search_group, initial):
        all_probabilities = self.__build_proba_dict(tups)
        if initial:
            print(all_probabilities)
            self.probabilities = all_probabilities
        # If the search group exists and is verb, limit tag possibilities
        if search_group == "verb":
            probabilities = {pos: proba for pos, proba in all_probabilities.items() if self.pos_is_verb(pos)}
        elif search_group == "noun":
            probabilities = {pos: proba for pos, proba in all_probabilities.items() if self.pos_is_noun(pos)}
        try:
            return max(probabilities.items(), key=operator.itemgetter(1))[0]
        except (ValueError, UnboundLocalError):
            return list(all_probabilities.keys())[0]

    @staticmethod
    def __build_proba_dict(tups):
        pos_tups = tups[1:]
        pos_tokens = pos_tups[0::2]
        pos_probas = pos_tups[1::2]
        proba_dict = dict(zip(pos_tokens, pos_probas))
        return {pos: proba for pos, proba in proba_dict.items() if proba >= PROBA_THRESHOLD}

