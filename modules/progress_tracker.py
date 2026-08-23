import os
import pandas as pd
from datetime import datetime


PROGRESS_PATH = "data/progress.csv"


def load_progress():

    if not os.path.exists(PROGRESS_PATH):

        return pd.DataFrame(
            columns=[
                "date",
                "topic",
                "difficulty",
                "score",
                "result"
            ]
        )

    return pd.read_csv(PROGRESS_PATH)


def save_progress(
    topic,
    difficulty,
    score,
    result
):

    df = load_progress()

    new_record = pd.DataFrame(
        [
            {
                "date": datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                ),
                "topic": topic,
                "difficulty": difficulty,
                "score": score,
                "result": result
            }
        ]
    )

    df = pd.concat(
        [df, new_record],
        ignore_index=True
    )

    df.to_csv(
        PROGRESS_PATH,
        index=False
    )

    return df


def get_learning_insights():

    df = load_progress()

    if df.empty:

        return None

    df["score"] = pd.to_numeric(
        df["score"],
        errors="coerce"
    )

    topic_scores = (
        df.groupby("topic")["score"]
        .mean()
        .sort_values(ascending=False)
    )

    strongest_topic = topic_scores.index[0]
    strongest_score = round(
        topic_scores.iloc[0],
        1
    )

    weakest_topic = topic_scores.index[-1]
    weakest_score = round(
        topic_scores.iloc[-1],
        1
    )

    average_score = round(
        df["score"].mean(),
        1
    )

    return {
        "strongest_topic": strongest_topic,
        "strongest_score": strongest_score,
        "weakest_topic": weakest_topic,
        "weakest_score": weakest_score,
        "average_score": average_score
    }
