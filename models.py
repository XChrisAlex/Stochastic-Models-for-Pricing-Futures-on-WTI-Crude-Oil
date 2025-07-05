import numpy as np
from scipy.optimize import least_squares

# Dummy model functions (replace with real ones later)
def model1(f, s, r, ttm):
    return lambda theta: f - s * np.exp((r - theta[0]) * ttm)

def model2(f, s, ttm):
    return lambda theta: f - s * np.exp(theta[0] + theta[1]*ttm + theta[2]*ttm**2)

def model3(f, s, ttm):
    return lambda theta: f - (s + theta[0]*ttm*np.sqrt(s) + (theta[0]**2*ttm**2/4)*(1 - theta[1]**2/(4*theta[0])))

def model4(f, s, ttm):
    return lambda theta: f - (s * np.exp(theta[1]*ttm) +
        (2*theta[0]*np.sqrt(s)/theta[1])*(np.exp(theta[1]*ttm) - np.exp(0.5*theta[1]*ttm)) +
        (theta[0]*(4*theta[0] - theta[2]**2)/(4*theta[1]**2))*(np.exp(0.5*theta[1]*ttm) - 1)**2)

def run_model(model_number, f, s, r, ttm, theta0, lb, ub):
    if model_number == 1:
        objective = model1(f, s, r, ttm)
    elif model_number == 2:
        objective = model2(f, s, ttm)
    elif model_number == 3:
        objective = model3(f, s, ttm)
    elif model_number == 4:
        objective = model4(f, s, ttm)
    else:
        raise ValueError("Invalid model number.")

    result = least_squares(objective, x0=theta0, bounds=(lb, ub))
    return {
        "theta": result.x,
        "resnorm": result.cost * 2,
        "rmse": (2 * result.cost / len(f))**0.5
    }

def predict_prices(model_number, s, r, ttm, theta):
    if model_number == 1:
        return s * np.exp((r - theta[0]) * ttm)

    elif model_number == 2:
        x_t = np.log(s)
        kappa = theta[1]
        return np.exp(
            x_t * np.exp(-kappa * ttm) +
            theta[0] * (1 - np.exp(-kappa * ttm)) +
            (theta[2] ** 2 / (4 * kappa)) * (1 - np.exp(-2 * kappa * ttm))
        )

    elif model_number == 3:
        a, sigma = theta
        return (
            s + a * ttm * np.sqrt(s) +
            (a ** 2 * ttm ** 2 / 4) * (1 - sigma ** 2 / (4 * a))
        )

    elif model_number == 4:
        a, b, sigma = theta
        return (
            s * np.exp(b * ttm) +
            (2 * a * np.sqrt(s) / b) * (np.exp(b * ttm) - np.exp(0.5 * b * ttm)) +
            (a * (4 * a - sigma ** 2) / (4 * b ** 2)) * (np.exp(0.5 * b * ttm) - 1) ** 2
        )

    else:
        raise ValueError("Invalid model number")