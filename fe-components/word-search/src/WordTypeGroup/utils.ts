export const specificWordType = (wordType: string): string => {
    if (!wordType.includes("(")) {
        return wordType;
    }
    const wordSplit = wordType.split("(");
    const bracketsContent = wordSplit[1].replace(")", "");
    const baseType = wordSplit[0].trim();
    return bracketsContent;
};
