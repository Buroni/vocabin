from .tree_tagger import VocaTagger

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
        self.voca_tagger = VocaTagger(lang=lang)

    def possible_groups(self):
        probas = self.voca_tagger.probabilities
        groups = []
        for pos, _ in probas.items():
            if self.voca_tagger.pos_is_verb(pos) and "verb" not in groups:
                groups.append("verb")
            elif self.voca_tagger.pos_is_noun(pos) and "noun" not in groups:
                groups.append("noun")
            elif self.voca_tagger.pos_is_adj(pos) and "adj" not in groups:
                groups.append("adj")
        return groups

    def get_pos_tag(self, word, search_group, initial):
        typ, group, pos = self.voca_tagger.word_tag_info(word, search_group, initial)
        return typ, group, pos

    def is_verb(self, word):
        return self.voca_tagger.is_verb(word)

    def is_noun(self, word):
        return self.voca_tagger.is_noun(word)

    def get_verb_lexeme(self, verb):
        return self.verbs.lexeme(verb)

    def get_noun_forms(self, noun):
        return list({self.singularize(noun), self.pluralize(noun)})

    def get_word_forms(self, word, search_group=None):
        if (self.is_verb(word) and search_group != "noun") or search_group == "verb":
            return self.get_verb_lexeme(word)
        elif (self.is_noun(word) and search_group != "verb") or search_group == "noun":
            return self.get_noun_forms(word)
        else:
            return [word]

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
