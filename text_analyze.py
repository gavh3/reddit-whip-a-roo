import matplotlib.pyplot as plt
import spacy
from collections import Counter
from wordcloud import WordCloud

# project modules
from reddit import get_newest_submissions

nlp = spacy.load("en_core_web_md")

def find_named_entities(corpus, entity_type):
    doc = nlp(corpus)
    labels = []
    for ent in doc.ents:
        if ent.label_ in [entity_type]:
            # print(ent.text, ent.start_char, ent.end_char, ent.label_)
            labels.append(ent.text)
    labels = [x[0] for x in Counter(labels).most_common(5)] # return most common product labels only
    return labels
    
def generate_word_cloud(labels):
    """
    Takes a pandas series and generates a wordcloud
    """
    fig, ax = plt.subplots(figsize=(3, 6))
    text = [a for b in labels.tolist() for a in b] # because the column values are lists, here we flatten to one list
    text_dict = Counter(text)
    wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate_from_frequencies(text_dict)
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    return fig

if __name__ == "__main__":
    submissions = get_newest_submissions(search_term="lexus suv", limit=20)
    submissions["product_labels"] = submissions["body"].apply(lambda x: find_named_product_entities(x))
    generate_word_cloud(submissions["body"])
