import numpy as np
import pandas as pd

def load_data(filename):
    date = pd.read_excel(filename, sheet_name='date', header=None).values
    spot = pd.read_excel(filename, sheet_name='Spot', header=None).values
    futures = pd.read_excel(filename, sheet_name='Futures', header=None).values
    rates = pd.read_excel(filename, sheet_name='r', header=None).values
    ttm = pd.read_excel(filename, sheet_name='ttm', header=None).values
    return date, spot, futures, rates, ttm

def flatten_data(futures_table, spot_prices_table, interest_rates_table, time_to_maturity_table):
    f_flat = futures_table.flatten()
    s_flat = spot_prices_table.flatten()
    r_flat = interest_rates_table.flatten()
    ttm_flat = time_to_maturity_table.flatten()
    return f_flat, s_flat, r_flat, ttm_flat

def process_data(f, s, r, num_prices):
    num_contracts = f.shape[1]
    futures_table = np.full((num_prices, num_contracts), np.nan)
    interest_rates_table = np.full((num_prices, num_contracts), np.nan)
    spot_prices_table = np.full((num_prices, num_contracts), np.nan)
    time_to_maturity_table = np.full((num_prices, num_contracts), np.nan)

    for i in range(num_contracts):
        valid_indices = ~np.isnan(f[:, i])
        valid_futures = f[valid_indices, i]
        valid_rates = r[valid_indices, i]
        valid_spot = s[valid_indices, i]

        if len(valid_futures) >= num_prices:
            futures_table[:, i] = valid_futures[-num_prices:]
            interest_rates_table[:, i] = valid_rates[-num_prices:]
            spot_prices_table[:, i] = valid_spot[-num_prices:]
            time_to_maturity_table[:, i] = np.linspace(1, 0, num_prices)
        else:
            raise ValueError(f"Column {i+1} has fewer than {num_prices} valid rows. Check your data.")

    return futures_table, spot_prices_table, interest_rates_table, time_to_maturity_table

def load_data_oos(filename):
    spot = pd.read_excel(filename, sheet_name='Spot', header=None).values
    futures = pd.read_excel(filename, sheet_name='Futures', header=None).values
    rates = pd.read_excel(filename, sheet_name='r', header=None).values
    ttm = pd.read_excel(filename, sheet_name='ttm', header=None).values
    return spot, futures, rates, ttm

