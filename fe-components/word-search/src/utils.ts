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

