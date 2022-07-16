# Importing necessary libraries
import uvicorn
import pickle
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

# Initialize fastAPI server
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Loading up the trained model
model = pickle.load(
    open('./model/saved_steps.pkl', 'rb'))
regressor = model["model"]
le_country = model["le_country"]
le_education = model["le_education"]

# Defining the model input types


class Candidate(BaseModel):
    country: str
    education: str
    experience: int

# Set up the home route

def shorten_categories(categories, cutoff):
    """
    If the value of a category is greater than the cutoff, then the category is mapped to itself.
    Otherwise, the category is mapped to 'Other'
    
    :param categories: the list of categories to be shortened
    :param cutoff: the minimum number of listings in a category to be considered a category
    :return: A dictionary with the key being the category and the value being the category or 'Other'
    """
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    """
    It takes a string as input, and returns a float
    
    :param x: The data to be cleaned
    :return: the value of x.
    """
    if x == 'More than 50 years':
        return 52
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    """
    If the string 'Bachelor’s degree' is in the input string, return 'Bachelor’s degree'. Otherwise, if
    the string 'Master’s degree' is in the input string, return 'Master’s degree'. Otherwise, if the
    string 'Professional degree' or 'Other doctoral' is in the input string, return 'Post grad'.
    Otherwise, return 'Less than a Bachelors'.
    
    :param x: The value being passed into the function
    :return: the value of the variable x.
    """
    
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

@app.get("/")
def read_root():
    return {"data": "Welcome to online employee hireability prediction model"}


@app.get("/salarystats/")
def read_model():
    df = pd.read_csv("../data/survey_results_public.csv")
    
# Converting the dataframe to json format.
    ed_s = json.loads(df.EdLevel.value_counts().rename_axis('ed').reset_index(name='count').to_json(orient="records"))
    age_s = json.loads(df.Age1stCode.value_counts().rename_axis('age').reset_index(name='count').to_json(orient="records"))
    state_s = json.loads(df.US_State.value_counts().rename_axis('state').reset_index(name='count').to_json(orient="records"))
    
# Selecting the columns that we need for our analysis.
    df = df[["Country", "EdLevel", "YearsCodePro",
             "Employment", "ConvertedCompYearly"]]
    df = df[df["ConvertedCompYearly"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)

# Filtering the dataframe to only include countries with more than 320 listings.
    country_map = shorten_categories(df.Country.value_counts(), 320)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedCompYearly"] <= 320000]
    df = df[df["ConvertedCompYearly"] >= 10000]
    df = df[df["Country"] != "Other"]

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    dtf = df.Country.value_counts().rename_axis('country').reset_index(name='counts')
    dtf2 = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True).rename_axis('country').reset_index(name='salary')
    
    
# Converting the dataframe to json format.
    result = dtf.to_json(orient="records")
    parsed = json.loads(result)
    
    result2 = dtf2.to_json(orient="records")
    parsed2 = json.loads(result2)
    
    return {"data": parsed,
            "data2" : parsed2,
            "age":age_s,
            "ed_level": ed_s,
            "state": state_s,}


# Setting up the prediction route
@app.post("/prediction/")
async def get_predict(data: Candidate):

    X = np.array([[data.country, data.education, data.experience]])
    X[:, 0] = le_country.transform(X[:, 0])
    X[:, 1] = le_education.transform(X[:, 1])
    X = X.astype(float)
    
# Predicting the salary of the candidate.
    salary = regressor.predict(X).tolist()[0]
    print(data)
    return {
        "data": {
            'prediction': salary,
        }
    }


# Configuring the server host and port
if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
