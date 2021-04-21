import pandas as pd
import streamlit as st
from transformers import pipeline
import plotly.express as px
from PIL import Image


@st.cache(allow_output_mutation=True)
def load_model():
    return pipeline("zero-shot-classification")


def classify(sequences: list, candidate_labels: list, multi_label=False):
    """
    Get the classification output

    Args:
        sequences: list - list of sequences you want to classify
        candidate_labels: list - Possible classfication labels
        multi_label: bool - binary or multiple labels

    Returns:
        res: list - list of predicted probabilities for each example
    """
    res = load_model()(sequences, candidate_labels, multi_label=multi_label)

    if isinstance(res, dict):
        return [res]

    return res


def output(res, multi_label):
    """
    Args:
        res: result from classifier
        multi_label: is it multilabel classification
    Returns:
        pd.DataFrame: Pandas DataFrames
    """

    sequences = []
    labels = []
    scores = []

    if multi_label:
        results = []
        for i in range(len(res)):
            record = {
                "example": res[i].get('sequence')
            }
            record.update(zip(res[i].get('labels'), res[i].get('scores')))
            results.append(record)
            print(results)
        return pd.DataFrame.from_records(results)
    else:

        for item in res:
            sequences.append(item.get("sequence"))
            labels.append(item.get('labels')[0])
            scores.append(item.get('scores')[0])

        return pd.DataFrame.from_dict(
            {
                "examples": sequences,
                "labels": labels,
                "scores": scores
            }
        )


def run():
    """
    Run the application
    """
    image = Image.open('zero-shot.png')

    st.sidebar.image(image)
    st.sidebar.info("You can use this app this app to do any simple classification without training")
    st.title("Zero-shot classification App")

    collect_list = lambda x: [str(item) for item in x.split(",")]

    sequences = st.text_input("Enter the examples separated by comma")
    candidate_labels = st.text_input("Enter the labels separated by comma")

    multi_label = st.checkbox("MultiLabel", [True, False])

    res = classify(collect_list(sequences), collect_list(candidate_labels), multi_label)
    data = output(res, multi_label)
    st.dataframe(data)

    if not multi_label:
        fig = px.bar(data, x='examples', y='scores', color='labels')
    else:
        fig = px.bar(data, x='example', y=collect_list(candidate_labels))
    st.plotly_chart(fig)


if __name__ == "__main__":
    run()
