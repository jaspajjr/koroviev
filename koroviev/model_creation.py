from __future__ import division
import pandas as pd
import numpy as np
from scipy.stats import poisson
import statsmodels.formula.api as smf
import statsmodels.api as sm
import json, os, sys

def get_fixtures_df():
    '''
    Read in the dataframe from a csv.
    '''
    df = pd.read_csv('~/working/github')

    return df

def train_model(results_df):
    '''
    This function trains the model on the specified df. The df must be in the
    proper format.
    '''
    model = smf.glm(
        formula='goals_scored_by_team ~ home_flag + team + opponent_team - 1',
        data=results_df, family=sm.families.Poisson())

    trained_model = model.fit()

    coeff_table = res.summary().tables[1]
    coeff_df = pd.read_html(coeff_table.as_html(), header=0)[0]

    col_names = ['param', 'coef', 'std_err', 'z', 'P', '95%']
    coeff_df.columns = col_names

    coeff_df.index = coeff_df['param']
    del coeff_df['param']

    train_model_dict = {}
    train_model['model'] = trained_model
    train_model['coeff_df'] = coeff_df
    return train_model_dict

def get_rho():
    rho = 0.9
    return rho

def get_gamma(df):
    gamma = np.mean(df['goals_scored_by_team']) / 2
    return gamma

def get_exp_goals_parameters(model, home_team, away_team):
    '''
    '''
    alpha_i = coeff_df.loc['team[{0}]'.format(home_team)]['coef']
    beta_i = coeff_df.loc['opponent_team[T.{0}]'.format(home_team)]['coef']
    alpha_j = coeff_df.loc['team[{0}]'.format(away_team)]['coef']
    beta_j = coeff_df.loc['opponent_team[T.{0}]'.format(away_team)]['coef']

    gamma = get_gamma()
    rho = get_rho()

    lambda_var = rho * gamma * np.exp(alpha_i) * np.exp(beta_j)
    mu_var = gamma * np.exp(alpha_j) * np.exp(beta_i)
    param_dict = {}
    param_dict['lambda_var'] = lambda_var
    param_dict['mu_var'] = mu_var

    return param_dict

def unpack_results(results_dict):
    '''
    '''
    if results_dict['home'] > results_dict['away']:
        return 'home'

    if results_dict['home'] == results_dict['away']:
        return 'draw'

    if results_dict['home'] < results_dict['away']:
        return 'away'

def game_result(param_dict):
    '''
    using the lambda and mu params for poisson distributions to get expected
    goals for the game.
    '''
    lambda_var = param_dict['lambda_var']
    mu_var = param_dict['mu_var']
    home_goals = poisson(lambda_var).rvs(1)
    away_goals = poisson(mu_var).rvs(1)
    goals_dict = {}
    goals_dict['home_goals'] = home_goals
    goals_dict['away_goals'] = away_goals

    return goals_dict

def calculate_all_repetitions(param_dict, repetitions):
    '''
    Takes $repetitions samples from the parametized poisson dictionaries.
    Returns a dataframe with every result from the model.
    '''
    results_variable = game_result(param_dict)
    results_list = []
    for x in xrange(repetitions):
        # if x % 1000: print x

        results_list.append(game_result(param_dict))
    results_df = pd.DataFrame({'result': results_list})
    return results_df

def get_game_posterior(home_team, away_team, trained_model, repetitions=None):
    '''
    Get posterior distribution of the expected game result between the two
    specified team, according to the given game.
    '''
    # Set number of repetitions for the posterior
    if repetitions is None:
        repetitions = 10000

    # get the csv
    results_df = get_fixtures_df()
    # train the model, return a fitted model, and a coefficient dataframe.
    train_model_dict = train_model(results_df)

    model = train_model_dict['model']
    coeff_df = train_model_dict['coeff_df']

    # get the parameters for lambda and gamma
    param_dict = get_exp_goals_parameters(model=model, home_team='Aston Villa',
        away_team='Liverpool')

    # get the expected number of goals given the parameters
    results_df = calculate_all_repetitions(param_dict, repetitions)
