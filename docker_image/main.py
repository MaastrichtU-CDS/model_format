from typing import List, Union
from fastapi import FastAPI
from oberije_2014_lung_survival import oberije_lung_survival

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/predict")
def predict(data: Union[dict, List[dict]]):
    """
    Calculate the probability of 2-year survival for a patient with given covariates.

    Parameters:
    - data: a dictionary containing the input data

    Returns:
    - probability: the probability of 2-year survival
    """
    model_obj = oberije_lung_survival()
    return model_obj.predict(data)

@app.get("/input_parameters")
def get_input_parameters():
    """
    Get the input parameters of the model.

    Returns:
    - input_parameters: a list of input parameters
    """
    model_obj = oberije_lung_survival()
    return model_obj.get_input_parameters()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)