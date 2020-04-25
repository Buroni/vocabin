# Tuple is (description, group, pos pattern regex)
pos_patterns = {
    "en": [
        ("Adverb", "misc",  r"RB.*"),
        ("Article", "misc",  r"DT"),
        ("Adjective", "misc",  r"JJ.*"),
        ("Conjunction", "misc",  r"CC"),
        ("Preposition", "misc",  r"IN"),
        ("Interjection", "misc",  r"UH"),
        ("Pronoun", "misc", r"(PP.*|WP.*)"),
        ("Noun (singular)", "noun", r"(NN|NP)$"),
        ("Noun (plural)", "noun", r"(NNS|NPS)"),
        ("Verb (modal)", "verb", r"(MD|VM0)"),
        ("Verb (base)", "verb",  r"(VV|VB)$"),
        ("Verb (past)", "verb",  r"(VVD|VBD)"),
        ("Verb (present participle / gerund)", "verb",  r"(VVG|VBG)"),
        ("Verb (past participle)", "verb",  r"(VVN|VBN)"),
        ("Verb (singular present)", "verb",  r"(VVZ|VBP|VBZ)"),
    ],
    "de": [
        ("Adverb", "misc",  r"ADV"),
        ("Article", "misc",  r"ART"),
        ("Adjective", "misc",  r"ADJ.*"),
        ("Conjunction", "misc",  r"KO.*"),
        ("Preposition", "misc",  r"APPR.*"),
        ("Interjection", "misc",  r"ITJ"),
        ("Pronoun", "misc", r"P(W|R|P|I|D).*"),
        ("Noun", "noun", r"N.*"),
        ("Verb (infinitive modal)", "verb", r"VMINF"),
        ("Verb (finite modal)", "verb", r"VMFIN"),
        ("Verb (base)", "verb",  r"(VVINF|VVIZU|VAINF)"),
        ("Verb (past participle)", "verb",  r"(VVPP|VAPP|VMPP)"),
        ("Verb (imperative)", "verb",  r"V.*IMP"),
        ("Verb (finite modal)", "verb",  r"VMFIN"),
        ("Verb (finite)", "verb",  r"V(V|A)FIN"),
    ],
    "es": [
        ("Adverb", "misc",  r"ADV"),
        ("Article", "misc",  r"ART"),
        ("Adjective", "misc",  r"ADJ"),
        ("Conjunction", "misc",  r"(CC.*|CQUE|CS.*)"),
        ("Preposition", "misc",  r"PREP"),
        ("Interjection", "misc",  r"ITJN"),
        ("Pronoun", "misc", r"(PP.*|REL|INT)"),
        ("Noun", "noun", r"(NC|NM.*)"),
        ("Verb (base)", "verb",  r"V.*inf"),
        ("Verb (present participle / gerund)", "verb",  r"V.*ger"),
        ("Verb (past participle)", "verb",  r"V.*adj"),
        ("Verb (finite)", "verb",  r"V.*fin"),
    ],
    "nl": [
        ("Adverb", "misc",  r"adv.*"),
        ("Article", "misc",  r"det__art"),
        ("Adjective", "misc",  r"adj.*"),
        ("Conjunction", "misc",  r"conj.*"),
        ("Preposition", "misc",  r"prep.*"),
        ("Interjection", "misc",  r"int"),
        ("Pronoun", "misc", r"(det__(demo|indef|poss|quest|rel)|pron.*)"),
        ("Noun (singular)", "noun", r"(nounsg|nounprop)"),
        ("Noun (plural)", "noun", r"nounpl"),
        ("Verb (base)", "verb",  r"verbinf"),
        ("Verb (singular past)", "verb",  r"verbpastsg"),
        ("Verb (plural past)", "verb",  r"verbpastpl"),
        ("Verb (plural past)", "verb",  r"verbpastpl"),
        ("Verb (present participle / gerund)", "verb",  r"verbpresp"),
        ("Verb (singular present)", "verb",  r"verbpressg"),
        ("Verb (plural present)", "verb",  r"verbprespl"),
        ("Verb (past participle)", "verb",  r"verbpapa"),
    ],
    "fr": [
        ("Adverb", "misc",  r"ADV"),
        ("Article", "misc",  r"DET:ART"),
        ("Adjective", "misc",  r"ADJ"),
        ("Conjunction", "misc",  r"KON"),
        ("Preposition", "misc",  r"PRP"),
        ("Interjection", "misc",  r"INT"),
        ("Pronoun", "misc", r"(DET:POS|PRO.*)"),
        ("Noun", "noun", r"(NAM|NOM)"),
        ("Verb (base)", "verb",  r"VER:infi"),
        ("Verb (past)", "verb",  r"VER:simp"),
        ("Verb (present participle / gerund)", "verb",  r"VER:ppre"),
        ("Verb (past participle)", "verb",  r"VER:pper"),
        ("Verb (future)", "verb",  r"VER:futu"),
        ("Verb (imperative)", "verb",  r"VER:impe"),
        ("Verb (conditional)", "verb",  r"VER:cond"),
        ("Verb (imperfect)", "verb",  r"VER:impf"),
        ("Verb (subjunctive imperfect)", "verb",  r"VER:subi"),
        ("Verb (subjunctive perfect)", "verb",  r"VER:subp"),
    ],
    "it": [
        ("Adverb", "misc",  r"ADV"),
        ("Article", "misc",  r"DET.*"),
        ("Adjective", "misc",  r"ADJ"),
        ("Conjunction", "misc",  r"CON"),
        ("Preposition", "misc",  r"PRE.*"),
        ("Interjection", "misc",  r"INT"),
        ("Pronoun", "misc", r"PRO.*"),
        ("Noun", "noun", r"(NPR|NOM)"),
        ("Verb (base)", "verb",  r"VER:infi"),
        ("Verb (reflexive base)", "verb",  r"VER:refl:infi"),
        ("Verb (past)", "verb",  r"VER:remo"),
        ("Verb (present participle / gerund)", "verb",  r"VER:(geru|ppre)"),
        ("Verb (past participle)", "verb",  r"VER:pper"),
        ("Verb (present)", "verb",  r"VER:pres"),
        ("Verb (future)", "verb",  r"VER:futu"),
        ("Verb (imperative)", "verb",  r"VER:impe"),
        ("Verb (conditional)", "verb",  r"VER:cond"),
        ("Verb (imperfect)", "verb",  r"VER:impf"),
        ("Verb (conjunctive imperfect)", "verb",  r"VER:cimp"),
        ("Verb (conjunctive present)", "verb",  r"VER:cpre"),
    ]
}
