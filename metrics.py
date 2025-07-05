def evaluate_maturity_classes(ttm, residuals, model_number):
    import numpy as np
    from plotting import plot_class_rmse

    maturity_classes = np.linspace(0, 1, 5)
    num_classes = len(maturity_classes) - 1
    class_sse = np.zeros(num_classes)
    class_rmse = np.zeros(num_classes)

    for j in range(num_classes):
        lower = maturity_classes[j]
        upper = maturity_classes[j + 1]
        ttm_mask = (ttm > lower) & (ttm <= upper)
        class_residuals = residuals[ttm_mask]

        if class_residuals.size > 0:
            class_sse[j] = np.sum(class_residuals**2)
            class_rmse[j] = np.sqrt(class_sse[j] / class_residuals.size)
        else:
            class_sse[j] = np.nan
            class_rmse[j] = np.nan

    print(f"📚 Maturity Class-Level Metrics (Model {model_number}):")
    for j in range(num_classes):
        print(f"  Class {j+1} [{maturity_classes[j]:.2f}, {maturity_classes[j+1]:.2f}]: "
              f"SSE = {class_sse[j]:.5f}, RMSE = {class_rmse[j]:.5f}")

    plot_class_rmse(maturity_classes, class_rmse, model_number)

import numpy as np
from plotting import plot_class_rmse_grouped

def evaluate_maturity_classes_all_models(ttm, all_residuals_dict):
    maturity_classes = np.linspace(0, 1, 5)
    num_classes = len(maturity_classes) - 1
    model_rmse = {}

    for model_num, residuals in all_residuals_dict.items():
        class_rmse = np.zeros(num_classes)
        for j in range(num_classes):
            lower = maturity_classes[j]
            upper = maturity_classes[j + 1]
            ttm_mask = (ttm > lower) & (ttm <= upper)
            class_res = residuals[ttm_mask]

            if class_res.size > 0:
                class_rmse[j] = np.sqrt(np.sum(class_res**2) / class_res.size)
            else:
                class_rmse[j] = np.nan

        model_rmse[model_num] = class_rmse

    plot_class_rmse_grouped(maturity_classes, model_rmse)
