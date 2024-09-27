
from math import log, exp

model_parameters = {
    'intercept': -0.5,
    'covariate_weights': {
        'gender': 0.8325, # male = 0, female = 1
        'who': -0.4395,
        'fev1': 0.0056,
        'lymph': -0.28002,
        'gtv': -0.7746
    }
}

def calculate_probability(gender, who, fev1, lymph, gtv):
    """
    Calculate the probability of 2-year survival for a patient with given covariates.
    This model is based on the following publication: Oberije C, De Ruysscher D, Houben A, et al. A Validated Prediction Model for Overall Survival From Stage III Non-Small Cell Lung Cancer: Toward Survival Prediction for Individual Patients. Int J Radiat Oncol Biol Phys. 2015;92(4):935-944. doi:10.1016/j.ijrobp.2015.03.030

    Parameters:
    - gender: 0 for male and 1 for female
    - who: WHO performance status (range: 0-4)
    - fev1: forced expiratory volume in 1 second (in liters)
    - lymph: number of positive lymph nodes (range: 0-10)
    - gtv: gross tumor volume (in cm^3, range 0-1000)
    """
    gtv = log(gtv)
    # Calculate the linear predictor
    linear_predictor = model_parameters['intercept']
    for covariate, weight in model_parameters['covariate_weights'].items():
        linear_predictor += weight * locals()[covariate]
    
    # Calculate the probability
    probability = 1 / (1 + exp(-exp(linear_predictor)))
    return probability