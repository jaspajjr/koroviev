from __future__ import division
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import poisson

class behemoth(object):
    """
    This class takes a dataframe of results, builds a weighted model for \lambda,
    \mu, \gamma, and \rho.

    - Gets the results
    - Fits the model
    - Make a prediction
    """

    def __init__(self, results_df):
        self.results_df = results_df
        self.model = None
        self.coeff_df = None
        self.rho = None
        self.gamma = None



    def train_model(self):
        """
        - This method trains the model.
        """
        model = smf.glm(
            formula='goals_scored_by_team ~ home_flag + team + opponent_team - 1',
            data=self.results_df,
            family=sm.families.Poisson())

        self.model = model.fit()

    def find_coefficients_df(self):
        """
        Gets the coefficient df from the model for use parametizing future
        predictions.
        """
        model = self.model()
        coeff_table = model().summary().tables[1]
        coeff_df = pd.read_html(coeff_table.as_html(), header=0)[0]

        col_names = ['param', 'coef', 'std_err', 'z', 'P', '95%']
        coeff_df.columns = col_names
        coeff_df.index = coeff_df['param']
        del coeff_df['param']

        self.coeff_df

    def _get_rho(self):
        """
        Returns the rho parameter.
        """
        self.rho = 0.9

    def _get_gamma(self):
        """
        Calculates the \gamma parameter.
        """
        self.gamma = np.mean(self.results_df['goals_scored_by_team']) / 2

    def _equation(self):
        """
        The function for the 
        """

    def predict(self, home_team, away_team):
        """
        Predicts the result of a game between the home team and the away_team.
        """
        pass
