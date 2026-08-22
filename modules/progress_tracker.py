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
