import pandas as pd
import pymorphy2
import nltk


nltk.download("punkt")
morph = pymorphy2.MorphAnalyzer()
prob_thresh = 0.5


def get_ner_dicts(
    text_file: str,
) -> tuple[dict[str, int], dict[str, int], dict[str, int]]:
    """
    A function that takes the name of a TXT-file.
    It preprocesses text and returns three dictionaries with named entities in it:
    - names,
    - surnames,
    - places.
    
    Args:
        text_file (str): name of TXT-file.

    Returns:
        tuple[
        dict[str, int], 
        dict[str, int], 
        dict[str, int]
        ]: names, surnames & places in the text.
    """
    with open(text_file, "r", encoding="utf-8") as gogol_file:
        text = gogol_file.read()

    names, surnames, places = {}, {}, {}

    for word in nltk.word_tokenize(text):
        for p in morph.parse(word):
            if "Name" in p.tag and p.score >= prob_thresh:
                _ = names.setdefault(p.normal_form, 0)
                names[p.normal_form] += 1
            elif "Surn" in p.tag and p.score >= prob_thresh:
                _ = surnames.setdefault(p.normal_form, 0)
                surnames[p.normal_form] += 1
            elif "Geox" in p.tag and p.score >= prob_thresh:
                _ = places.setdefault(p.normal_form, 0)
                places[p.normal_form] += 1
    return names, surnames, places


def saving(ner_dict: dict[str, int], file_name: str) -> None:
    """
    A function that a dictionary with named entities and the name of a CSV-file.
    It sorts the dictionary, filters it and saves as a DataFrame in CSV-file.
    
    Args:
        ner_dict (dict[str, int]): NER dictionary.
        file_name (str): name of CSV-file

    Returns:
        None
    """
    ner_tuple = sorted(ner_dict.items(), key=lambda x: x[1], reverse=True)
    ner_dict = {item[0].capitalize(): item[1] for item in ner_tuple if item[1] > 4}
    pd.DataFrame.from_dict(ner_dict, orient="index", columns=["Counts"]).to_csv(
        file_name
    )


def main():
    dict_names, dict_surnames, dict_places = get_ner_dicts("gogol.txt")
    saving(dict_names, "names.csv")
    saving(dict_surnames, "surnames.csv")
    saving(dict_places, "places.csv")


if __name__ == "__main__":
    main()
