export const specificWordType = (wordType: string): string => {
    const wordSplit = wordType.split("(");
    const bracketsContent = wordSplit[1].replace(")", "");
    const baseType = wordSplit[0].trim();
    return bracketsContent;
};
