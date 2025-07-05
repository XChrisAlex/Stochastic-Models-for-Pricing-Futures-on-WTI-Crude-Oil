import numpy as np
import pandas as pd
from preprocessing import load_data, process_data, flatten_data, load_data_oos

# Load Excel data
path = 'DATASETORG.xlsx'
_, s, f, r, _ = load_data(path)

if r.shape[1] == 1:
    r = np.repeat(r, f.shape[1], axis=1)

if s.shape[1] == 1:
    s = np.repeat(s, f.shape[1], axis=1)

# Process data and flatten
f_table, s_table, r_table, ttm_table = process_data(f, s, r, 245)
f_flat, s_flat, r_flat, ttm_flat = flatten_data(f_table, s_table, r_table, ttm_table)

# Print shapes to confirm everything worked
print("Shapes:")
print("Futures:", f_flat.shape)
print("Spot:", s_flat.shape)
print("Rates:", r_flat.shape)
print("TTM:", ttm_flat.shape)

from models import run_model

# User choice
model_choice = 'all'  #choose between: 'all', 1, 2, 3, 4

# Parameter setup for each model
model_params = {
    1: {"theta0": [0.01], "lb": [-1], "ub": [1]},
    2: {"theta0": [0.1, 0.001, 0.01], "lb": [-1, 0, 0], "ub": [2, 1, 2]},
    3: {"theta0": [1.1, 0.01], "lb": [-2, 0], "ub": [20, 5]},
    4: {"theta0": [0.1, -0.1, 0.5], "lb": [0, -5, 0.5], "ub": [3.5, 0, 2.5]},
}


from plotting import plot_model_fit


# Run models -- you cant see all models plots at once, you have to choose between 1-4, else, you will just have the last model plot
results = {}  # ✅ always define this dictionary

# Run models
if model_choice == 'all':
    for i in range(1, 5):
        print(f"\n🔹 Running Model {i}")
        res = run_model(i, f_flat, s_flat, r_flat, ttm_flat, **model_params[i])
        results[i] = res
        print(f"Model {i} results:")
        for key, value in res.items():
            print(f"  {key}: {value}")
else:
    res = run_model(model_choice, f_flat, s_flat, r_flat, ttm_flat, **model_params[model_choice])
    results[model_choice] = res  # ✅ store single model result in the dictionary
    print(f"Model {model_choice} results:", res)
    
    # Plot the selected model
    theta_total = res["theta"]
    plot_model_fit(int(model_choice), f_flat, s_flat, r_flat, ttm_flat, theta_total)


from preprocessing import load_data_oos

s_oos, f_oos, r_oos, ttm_oos = load_data_oos("DATASETORG_OFS.xlsx")
# ✅ Flatten out-of-sample data
s_flat_oos = s_oos.flatten()
f_flat_oos = f_oos.flatten()
r_flat_oos = r_oos.flatten()
ttm_flat_oos = ttm_oos.flatten()

from models import predict_prices


print("\n📉 Out-of-Sample Evaluation:")

if model_choice == 'all':
    models_to_evaluate = range(1, 5)
else:
    models_to_evaluate = [model_choice]

for i in models_to_evaluate:
    theta = results[i]["theta"]
    f_pred_oos = predict_prices(i, s_flat_oos, r_flat_oos, ttm_flat_oos, theta)
    residuals_oos = f_flat_oos - f_pred_oos
    resnorm = np.sum(residuals_oos**2)
    rmse = np.sqrt(resnorm / len(f_flat_oos))

    print(f"Model {i}:")
    print(f"  Residual Norm (OOS): {resnorm:.4f}")
    print(f"  RMSE (OOS):          {rmse:.4f}")

# Store daily metrics per model
daily_metrics_all_models = {}

for i in models_to_evaluate:
    theta = results[i]["theta"]
    f_pred_oos = predict_prices(i, s_flat_oos, r_flat_oos, ttm_flat_oos, theta)

    # Reshape predicted and actual
    f_pred_matrix = f_pred_oos.reshape(f_oos.shape)
    f_actual_matrix = f_oos.reshape(f_oos.shape)

    # Residuals
    residuals_matrix = f_actual_matrix - f_pred_matrix

    # Initialize daily SSE/RMSE
    num_days, num_contracts = f_oos.shape
    daily_sse = np.zeros(num_days)
    daily_rmse = np.zeros(num_days)

    for day in range(num_days):
        residuals_day = residuals_matrix[day, :]
        residuals_day = residuals_day[~np.isnan(residuals_day)]
        daily_sse[day] = np.sum(residuals_day**2)
        if residuals_day.size > 0:
            daily_rmse[day] = np.sqrt(daily_sse[day] / residuals_day.size)
        else:
            daily_rmse[day] = np.nan

    # Store as DataFrame
    df = pd.DataFrame({
        "Day": np.arange(1, num_days + 1),
        "Daily_SSE_Total": daily_sse,
        "Daily_RMSE_Total": daily_rmse
    })
    daily_metrics_all_models[i] = df

# 🔽 Display all daily metrics
for i, df in daily_metrics_all_models.items():
    print(f"\n📊 Daily Metrics (Total Parameters) - Model {i}:")
    print(df)

from plotting import plot_daily_rmse_comparison

# ✅ Plot Daily RMSE Comparison
plot_daily_rmse_comparison(daily_metrics_all_models)    

from metrics import evaluate_maturity_classes
if model_choice in [1, 2, 3, 4]:
    evaluate_maturity_classes(ttm_flat_oos, residuals_oos, i)

from metrics import evaluate_maturity_classes_all_models

if model_choice == 'all':
    all_residuals_dict = {}
    for i in range(1, 5):
        theta = results[i]["theta"]
        f_pred_oos = predict_prices(i, s_flat_oos, r_flat_oos, ttm_flat_oos, theta)
        residuals_oos = f_flat_oos - f_pred_oos
        resnorm = np.sum(residuals_oos**2)
        rmse = np.sqrt(resnorm / len(f_flat_oos))

        print(f"Model {i}:")
        print(f"  Residual Norm (OOS): {resnorm:.4f}")
        print(f"  RMSE (OOS):          {rmse:.4f}")
        
        all_residuals_dict[i] = residuals_oos

    # 🔽 Single grouped bar chart
    evaluate_maturity_classes_all_models(ttm_flat_oos, all_residuals_dict)