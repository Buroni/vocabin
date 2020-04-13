export const buildQueryString = (params) => {
    if (!params) return "";
    const esc = encodeURIComponent;
    return Object.keys(params)
        .filter(k => params[k] !== "")
        .map(k => esc(k) + '=' + esc(params[k]))
        .join('&');
};

export const noResults = (res) => {
    return res.sentences.every(r => r.sentences.length === 0)
};

export const posTagToReadable = (pos) => {
    pos = pos.split(" ")[0];
    if (pos.includes("JJ")) {
        return "Adjective";
    }
    if (pos.includes("RB")) {
        return "Adverb";
    }
    if (pos === "IN") {
        return "Preposition / Conjunction";
    }
    if (pos === "DT") {
        return "Determiner";
    }
    if (pos === "UH") {
        return "Interjection";
    }
    if (pos === "MD") {
        return "Modal";
    }
    if (pos === "RP") {
        return "Particle";
    }
    if (pos === "CC") {
        return "Co-ordinating conjunction";
    }
    if (["NN", "NNP"].includes(pos)) {
        return "Noun (singular)";
    }
    if (["NNS", "NNPS"].includes(pos)) {
        return "Noun (plural)"
    }
    if (pos === "VB") {
        return "Verb";
    }
    if (pos === "VBD") {
        return "Verb (past)";
    }
    if (pos === "VBG") {
        return "Verb (gerund)";
    }
    if (pos === "VBN") {
        return "Verb (past part.)";
    }
    if (["VBP", "VBZ"].includes(pos)) {
        return "Verb (present)"
    }
    if (["WDT", "WP", "WP$", "WRB"].includes(pos)) {
        return "Wh- word"
    }
    return "Unknown type";
}
