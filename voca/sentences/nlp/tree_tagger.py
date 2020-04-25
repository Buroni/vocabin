import re
import treetaggerwrapper
from .pos_patterns import pos_patterns


class VocaTagger:
    def __init__(self, lang):
        self.tagger = treetaggerwrapper.TreeTagger(TAGLANG=lang)
        self.pos_patterns = pos_patterns[lang]
        self.lang = lang

    def tag_word(self, word):
        tag = self.tagger.tag_text(word)[0]
        print(tag)
        return tag.split("\t")[1]

    def word_tag_info(self, word):
        pos = self.tag_word(word)
        for description, cat, pattern in self.pos_patterns:
            if re.match(pattern, pos):
                return description, cat, pos
        return "Unknown type", "unk", None

    def is_noun(self, word):
        pos = self.tag_word(word)
        if self.lang in ["de", "es", "fr", "it", "en"]:
            return pos[0] == "N"
        elif self.lang == "nl":
            return pos[0:4] == "noun"

    def is_verb(self, word):
        pos = self.tag_word(word)
        if self.lang in ["de", "es", "fr", "it"]:
            return pos[0] == "V"
        elif self.lang == "en":
            return pos[0] == "V" or pos == "MD"
        elif self.lang == "nl":
            return pos[0] == "v"
        return False
