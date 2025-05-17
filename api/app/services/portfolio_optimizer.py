import pandas as pd
import numpy as np
import io
from scipy.optimize import minimize
import json
from fastapi import UploadFile

class PortfolioOptimizer:
    def __init__(self, data_file, risk_level, max_weight):
        self.data_file: UploadFile = data_file
        self.risk_level: float = risk_level
        self.max_weight: float = max_weight

    def read_and_clean_file(self):

        file_data = self.data_file.file.read().decode("utf-8")
        df = pd.read_csv(io.StringIO(file_data), encoding='utf-8', delimiter=',')
        df.set_index(df.columns[0], inplace=True)  # Establecer fechas como índice
        df.dropna(how='all', axis=1, inplace=True)  # Eliminar columnas vacías
        df.fillna(0, inplace=True)  # Llenar valores faltantes
        return df

    def calculate_cvar(self, returns, alpha=0.95):
        cvars = {}
        for column in returns.columns:
            sorted_returns = returns[column].sort_values()
            var = np.percentile(sorted_returns, (1 - alpha) * 100)
            cvar = sorted_returns[sorted_returns <= var].mean()
            cvars[column] = cvar
        return cvars

    def optimize_portfolio(self, returns, cvars, max_weight):
        assets = list(cvars.keys())
        init_weights = np.array([1 / len(assets)] * len(assets))

        def portfolio_cvar(weights):
            return sum(weights[i] * cvars[asset] for i, asset in enumerate(assets))

        constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
        bounds = [(0, max_weight)] * len(assets)

        result = minimize(portfolio_cvar, init_weights, method='SLSQP', bounds=bounds, constraints=constraints)
        return {assets[i]: round(result.x[i], 6) for i in range(len(assets))}

    def generate_output(self, optimal_weights):
        return json.dumps({"optimal_portfolio": optimal_weights}, indent=4)

