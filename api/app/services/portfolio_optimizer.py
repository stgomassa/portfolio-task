import io
import json
import pandas as pd
from pypfopt import EfficientFrontier, risk_models, expected_returns
class PortfolioOptimizer:
    def __init__(self, file, risk_level: float, max_weight: float):
        self.file = file
        self.risk_level = risk_level
        self.max_weight = max_weight
        self.df = None

    def clean_data(self):
        '''Read and parse CSV file. Clean data from empty values. Sets the index to the first column.'''
        try:
            file_data = self.file.file.read().decode("utf-8")
            self.df = pd.read_csv(io.StringIO(file_data), encoding='utf-8', delimiter=',')
        except pd.errors.EmptyDataError:
            raise ValueError("The provided CSV file is empty")
        except Exception as e:
            raise ValueError(f"Error reading CSV file: {str(e)}")

        try:
            self.df.set_index(self.df.columns[0], inplace=True)
            self.df.dropna(how='all', axis=1, inplace=True)
            self.df.fillna(0, inplace=True)
        except Exception as e:
            raise ValueError(f"Error processing data: {str(e)}")

    def optimize_portfolio(self):
        '''Optimize portfolio implementing Markowitz Mean-Variance Model.'''
        if self.df is None:
            raise ValueError("Data not loaded. Run clean_data() first.")

        # Calculate expected returns and sample covariance
        try:
            mu = expected_returns.mean_historical_return(self.df, returns_data=True)
            S = risk_models.sample_cov(self.df)
        except Exception as e:
            raise ValueError(f"Error calculating returns and covariance: {str(e)}")

        # Create the Efficient Frontier object
        try:
            ef = EfficientFrontier(mu, S, weight_bounds=(0, self.max_weight))
        except Exception as e:
            raise ValueError(f"Error creating Efficient Frontier: {str(e)}")

        # Maximize Sharpe ratio
        try:
            ef.max_sharpe()
        except Exception as e:
            raise ValueError(f"Error in Sharpe ratio maximization: {str(e)}")

        # Clean weights and store them
        try:
            cleaned_weights = ef.clean_weights()
            self.optimal_weights = {ticker: round(weight, 6) for ticker, weight in cleaned_weights.items()}
        except Exception as e:
            raise ValueError(f"Error processing optimal weights: {str(e)}")


    def get_result(self):
        try:
            if not hasattr(self, 'optimal_weights'):
                raise ValueError("Portfolio not optimized. Run optimize_portfolio() first.")
            return json.dumps({"optimal_portfolio": self.optimal_weights}, indent=4)
        except Exception as e:
            raise ValueError(f"Error generating result: {str(e)}")
