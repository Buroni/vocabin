sen_features = {
    "en": {
        "sentence_length": [10, 20, 30],
        "word_length_thresh": 11
    },
    "de": {
        "sentence_length": [10, 20, 30],
        "word_length_thresh": 14
    },
    "fr": {
        "sentence_length": [10, 20, 30],
        "word_length_thresh": 13
    },
    "es": {
        "sentence_length": [10, 20, 30],
        "word_length_thresh": 11
    },
    "it": {
        "sentence_length": [10, 20, 30],
        "word_length_thresh": 12
    },
    "nl": {
        "sentence_length": [10, 20, 30],
        "word_length_thresh": 12
    }
}


class NLP:
    def __init__(self, lang):
        if lang == "en":
            from pattern.en import parse, pluralize, singularize, verbs
        elif lang == "de":
            from pattern.de import parse, pluralize, singularize, verbs
        elif lang == "fr":
            from pattern.fr import parse, pluralize, singularize, verbs
        elif lang == "es":
            from pattern.es import parse, pluralize, singularize, verbs
        elif lang == "it":
            from pattern.it import parse, pluralize, singularize, verbs
        elif lang == "nl":
            from pattern.nl import parse, pluralize, singularize, verbs
        else:
            raise NotImplementedError(f"Language code {lang} not supported.")
        self.parse = parse
        self.pluralize = pluralize
        self.singularize = singularize
        self.verbs = verbs
        self.lang = lang

    def get_pos_tag(self, word):
        pos = self.parse(word, chunks=False, relations=False).split("/")[1]
        # A bug in Pattern causes singular nouns to be tagged as plural.
        if pos == "NN" and word.lower() == self.pluralize(word).lower():
            return "NNS"
        return pos

    def is_verb(self, word):
        pos = self.get_pos_tag(word)
        return pos[0] == "V"

    def is_noun(self, word):
        pos = self.get_pos_tag(word)
        return pos[0] == "N"

    def get_verb_lexeme(self, verb):
        return self.verbs.lexeme(verb)

    def get_noun_forms(self, noun):
        pos = self.get_pos_tag(noun)
        if pos in ["NNS", "NNPS"]:
            return [noun, self.singularize(noun)]
        return [noun, self.pluralize(noun)]

    def get_word_forms(self, word):
        if self.is_verb(word):
            return self.get_verb_lexeme(word)
        elif self.is_noun(word):
            return self.get_noun_forms(word)
        else:
            return [word]

    def build_content_filter(self, word, all_forms):
        if self.is_verb(word) and all_forms == "true":
            lexeme = self.get_verb_lexeme(word)
            word_str = r"|".join(lexeme)
        elif self.is_noun(word) and all_forms == "true":
            forms = self.get_noun_forms(word)
            word_str = r"|".join(forms)
        else:
            word_str = word
        return r"\b(" + word_str + r")\b"

    def build_difficulty_filter(self, difficulty):
        lang_features = sen_features[self.lang]
        lang_sen_features = lang_features["sentence_length"]
        if difficulty == 0:
            return {
                "sentence_length__lte": lang_sen_features[0],
                "avg_word_length__lte": lang_features["word_length_thresh"]
            }
        elif difficulty == 1:
            return {
                "sentence_length__lte": lang_sen_features[1],
                "sentence_length__gt": lang_sen_features[0],
            }
        return {
            "sentence_length__gt": lang_sen_features[2],
        }
