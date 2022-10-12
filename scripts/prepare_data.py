# https://www.kaggle.com/datasets/averkij/reddit-jokes-dataset
# https://github.com/taivop/joke-dataset/blob/master/reddit_jokes.json

import pandas as pd
import json

df_jokes = pd.read_csv("data/sources/jokes.csv")
df_jokes["joke"] = df_jokes["Question"] + "\n" + df_jokes["Answer"]

with open("data/sources/reddit_jokes.json") as f:
    df_reddit_jokes = pd.DataFrame(json.loads(f.read()))
df_reddit_jokes["joke"] = df_reddit_jokes["title"] + "\n" + df_reddit_jokes["body"]

df_shortjokes = pd.read_csv("data/sources/shortjokes.csv")
df_shortjokes["joke"] = df_shortjokes["Joke"]

with open("data/sources/stupidstuff.json") as f:
    df_stupidstuff = pd.DataFrame(json.loads(f.read()))
df_stupidstuff["joke"] = df_stupidstuff["body"]

with open("data/sources/wocka.json") as f:
    df_wocka = pd.DataFrame(json.loads(f.read()))
df_wocka["joke"] = df_wocka["body"]

df = pd.concat(
    [
        df_jokes[["joke"]],
        df_reddit_jokes[["joke"]],
        df_shortjokes[["joke"]],
        df_stupidstuff[["joke"]],
        df_wocka[["joke"]],
    ]
)

df["joke"] = df["joke"].str.strip()
df = df[df["joke"] > ""]


def clean(s):
    return "\n".join([x.strip() for x in s.split("\n")])


df["joke"] = df["joke"].apply(clean)
df = df.drop_duplicates("joke")
df = df.sample(len(df))


df["len"] = df["joke"].apply(len)
df = df[df["len"] <= 512]

for p in df["joke"].sample(20):
    print(p, "\n---------")


df.to_csv("data/prepared_data.csv", index=False)
