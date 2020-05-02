import operator
import re
from .treetaggerwrapper import TreeTagger, make_tags
from .pos_patterns import pos_patterns


class VocaTagger:
    def __init__(self, lang):
        self.tagger = TreeTagger(TAGLANG=lang)
        self.pos_patterns = pos_patterns[lang]
        self.lang = lang

    def tag_word(self, word, search_group=None):
        tag = make_tags(self.tagger.tag_text(word), allow_extra=True)[0]
        return self.__most_likely_tag(tag.extra, search_group)

    def word_tag_info(self, word, search_group):
        pos = self.tag_word(word, search_group)
        for description, cat, pattern in self.pos_patterns:
            if re.match(pattern, pos):
                return description, cat, pos
        return "Unknown type", "unk", None

    def is_noun(self, word):
        pos = self.tag_word(word)
        return self.__pos_is_noun(pos)

    def is_verb(self, word):
        pos = self.tag_word(word)
        return self.__pos_is_verb(pos)

    def __pos_is_noun(self, pos):
        if self.lang in ["de", "es", "fr", "it", "en"]:
            return pos[0] == "N"
        elif self.lang == "nl":
            return pos[0:4] == "noun"

    def __pos_is_verb(self, pos):
        if self.lang in ["de", "es", "fr", "it"]:
            return pos[0] == "V"
        elif self.lang == "en":
            return pos[0] == "V" or pos == "MD"
        elif self.lang == "nl":
            return pos[0] == "v"
        return False

    def __most_likely_tag(self, tups, search_group):
        probabilities = self.__build_proba_dict(tups)
        # If the search group exists and is verb, limit tag possibilities to verbs
        if search_group == "verb":
            probabilities = {pos: proba for pos, proba in probabilities.items() if self.__pos_is_verb(pos)}
        return max(probabilities.items(), key=operator.itemgetter(1))[0]

    @staticmethod
    def __build_proba_dict(tups):
        pos_tups = tups[1:]
        pos_tokens = pos_tups[0::2]
        pos_probas = pos_tups[1::2]
        return dict(zip(pos_tokens, pos_probas))

