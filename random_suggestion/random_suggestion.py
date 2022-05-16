import json

import pandas as pd

import constants


def recommender(df):
    recommended = df.sample(n=5)
    return recommended["recipe_id"]


if __name__ == "__main__":
    df = pd.read_csv(constants.ROOT+"/resources/recipe_data.csv")
    recommendations = recommender(df)
    recipes = {}
    for recipe_id in recommendations:
        recipes[recipe_id] = (df[df["recipe_id"] == recipe_id]["recipeName"]).tolist()[0]
    print(json.dumps(recipes, indent=4))
