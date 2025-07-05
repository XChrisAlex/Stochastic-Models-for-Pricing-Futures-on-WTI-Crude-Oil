import numpy as np
import matplotlib.pyplot as plt

def plot_model_fit(model_number, f_flat, s_flat, r_flat, ttm_flat, theta_total):
    
    #Generate plots to assess model fit:
    #1. Actual vs Predicted
    #2. Residuals vs TTM
    #3. Actual and Predicted over TTM#
    

    # Generate predicted futures prices
    if model_number == 1:
        f_pred = s_flat * np.exp((r_flat - theta_total[0]) * ttm_flat)

    elif model_number == 2:
        x_t = np.log(s_flat)
        kappa = theta_total[1]
        f_pred = np.exp(
            x_t * np.exp(-kappa * ttm_flat) +
            theta_total[0] * (1 - np.exp(-kappa * ttm_flat)) +
            (theta_total[2]**2 / (4 * kappa)) * (1 - np.exp(-2 * kappa * ttm_flat))
        )

    elif model_number == 3:
        a, sigma = theta_total
        f_pred = (
            s_flat + a * ttm_flat * np.sqrt(s_flat) +
            (a**2 * ttm_flat**2 / 4) * (1 - sigma**2 / (4 * a))
        )

    elif model_number == 4:
        a, b, sigma = theta_total
        f_pred = (
            s_flat * np.exp(b * ttm_flat) +
            (2 * a * np.sqrt(s_flat) / b) * (np.exp(b * ttm_flat) - np.exp(0.5 * b * ttm_flat)) +
            (a * (4 * a - sigma**2) / (4 * b**2)) * (np.exp(0.5 * b * ttm_flat) - 1)**2
        )
    else:
        raise ValueError("Invalid model number. Must be 1–4.")

    # Residuals
    residuals = f_flat - f_pred


    # Plot 1: Actual vs Predicted
    plt.figure(figsize=(6, 5))
    plt.scatter(f_flat, f_pred, color='blue', label='Predicted vs Actual')
    min_f, max_f = min(f_flat), max(f_flat)
    plt.plot([min_f, max_f], [min_f, max_f], 'r--', label='y = x')
    plt.xlabel("Actual Futures Prices")
    plt.ylabel("Predicted Futures Prices")
    plt.title(f"Model {model_number} – Actual vs Predicted Futures Prices")
    plt.grid(True)
    plt.legend()
    plt.show()

    # Plot 2: Residuals vs TTM
    plt.figure(figsize=(6, 5))
    plt.scatter(ttm_flat, residuals, color='blue')
    plt.axhline(0, color='red', linestyle='--')
    plt.xlabel("Time-to-Maturity (TTM)")
    plt.ylabel("Residuals (Actual - Predicted)")
    plt.title(f"Model {model_number} - Residuals vs Time-to-Maturity")
    plt.grid(True)
    plt.show()

    # Plot 3: Actual and Predicted over TTM
    plt.figure(figsize=(6, 5))
    plt.plot(ttm_flat, f_flat, 'b.', label='Actual Prices')
    plt.plot(ttm_flat, f_pred, 'r.', label='Predicted Prices')
    plt.xlabel("Time-to-Maturity (TTM)")
    plt.ylabel("Futures Prices")
    plt.title(f"Model {model_number} - Actual vs Predicted over Time-to-Maturity")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_daily_rmse_comparison(daily_metrics_all_models):
    """
    Plots daily RMSE comparison across models.

    Parameters:
        daily_metrics_all_models (dict): Keys are model numbers, values are DataFrames with columns:
            - 'Day'
            - 'Daily_RMSE_Total'
    """
    plt.figure(figsize=(8, 5))
    for model_num, df in daily_metrics_all_models.items():
        plt.plot(df["Day"], df["Daily_RMSE_Total"], label=f"Model {model_num}", linewidth=1.5)

    plt.xlabel("Day")
    plt.ylabel("Daily RMSE")
    plt.title("Daily RMSE Comparison Across Models")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_class_rmse(maturity_classes, class_rmse, model_number):
    import matplotlib.pyplot as plt
    midpoints = 0.5 * (maturity_classes[:-1] + maturity_classes[1:])
    plt.figure(figsize=(6, 4))
    plt.bar(midpoints, class_rmse, width=np.diff(maturity_classes), edgecolor='black')
    plt.xlabel("Maturity Class (Years)")
    plt.ylabel("RMSE (Out-of-Sample)")
    plt.title(f"Model {model_number} – RMSE by Maturity Class (OOS)")
    plt.grid(True)
    plt.show()

def plot_class_rmse_grouped(maturity_classes, model_rmse_dict):
    models = sorted(model_rmse_dict.keys())
    num_classes = len(maturity_classes) - 1
    bar_width = 0.2
    x = np.arange(num_classes)

    plt.figure(figsize=(8, 5))
    for i, model in enumerate(models):
        rmse = model_rmse_dict[model]
        offset = (i - len(models)/2) * bar_width + bar_width/2
        plt.bar(x + offset, rmse, width=bar_width, label=f"Model {model}")

    class_labels = [f"[{maturity_classes[i]:.2f}, {maturity_classes[i+1]:.2f}]" for i in range(num_classes)]
    plt.xticks(x, class_labels)
    plt.xlabel("Maturity Class (Years)")
    plt.ylabel("RMSE (Out-of-Sample)")
    plt.title("RMSE by Maturity Class for All Models (OOS)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()