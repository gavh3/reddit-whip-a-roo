import time
import streamlit as st
from collections import Counter
from PIL import Image

# import project modules
from reddit import get_newest_submissions
from text_analyze import find_named_entities, generate_word_cloud
from utils import plot_barh


st.set_page_config(page_title="Reddit Whip-a-roo")
title_container = st.container()
col1, col2 = st.columns((1, 4))
image = Image.open('cybertruck.png')
description = """
A car is one of the largest purchases many of us will ever make. So why not base it on opinions from strangers on Reddit?

Whether you want a "daily driver" or [the car with wing doors from that movie](https://en.wikipedia.org/wiki/DeLorean_time_machine), take us for a spin and see what lands.
"""

with title_container:
    with col1:
        st.write("")
        st.write("")
        st.write("")
        st.image(image, use_column_width=None)
    with col2:
        st.title("Reddit Finds Me A Car")
        st.markdown(body=description)


with st.sidebar.form("search-form"):
    selected_search_term = st.text_input("Search term")
    selected_num_results = st.number_input("Number of submissions", min_value=1, max_value=1000, value=25)

    search_form_submit = st.form_submit_button("See results")

if search_form_submit:
    with st.spinner("Scraping Reddit.."):
        s = time.perf_counter()
        submissions = get_newest_submissions(search_term=selected_search_term, limit=selected_num_results)
        submissions["body_product_labels"] = submissions["body"].apply(lambda x: find_named_entities(x, "PRODUCT"))
        submissions["comment_product_labels"] = submissions["top_comment"].apply(lambda x: find_named_entities(x, "PRODUCT"))
        submissions["body_org_labels"] = submissions["body"].apply(lambda x: find_named_entities(x, "ORG"))
        submissions["comment_org_labels"] = submissions["top_comment"].apply(lambda x: find_named_entities(x, "ORG"))
        submissions = submissions[["created", "title", "body_product_labels", "body_org_labels", "comment_product_labels", "comment_org_labels"]]
        duration = time.perf_counter() - s
    if len(submissions) > 0:
        st.info(f"Done in {duration:0.2f} seconds")
        body_labels_wc = generate_word_cloud(submissions["body_product_labels"])
        st.pyplot(body_labels_wc)
        st.subheader("Top brands")
        brands_list = [a for b in submissions["body_org_labels"].tolist() for a in b]
        brands_count = Counter(brands_list)
        brands_count = sorted(brands_count.items(), key=lambda i: -i[1])[:10] # get the top 10 most common brands
        brands_count = sorted(dict(brands_count).items(), key=lambda i: i[1]) # reverse the order for the right plot sequence
        st.pyplot(
            plot_barh(
                y=[x[0] for x in brands_count],
                width=[x[1] for x in brands_count])
        )
        st.subheader("Top 10 results found")
        st.dataframe(submissions.head(10))