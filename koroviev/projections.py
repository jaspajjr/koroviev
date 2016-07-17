import pandas as pd
import numpy as np
from scipy.stats import binom

def calculate_returns_after_N_periods(initial_capital, N, binomial_model):
    '''
    '''
    capital_progress = [initial_capital]
    for game in xrange(N):
        capital = capital_progress[-1]
        stake = capital * 0.1
        success = binomial_model.rvs(1)
        if success == 0:
            result = round(stake + capital, 2)
            capital_progress.append(result)
        elif success == 1:
            result = round((-1 * stake) + capital, 2)
            capital_progress.append(result)

    result_array = np.array(capital_progress)

    return result_array

def unpack_cmigc_kwargs(kwargs):
    '''
    Given the kwargs for cmigc, this unpacks the kwargs passed as an argument,
    if vital arguments are not included in the kwargs, they will be replaced
    with default values.
    '''
    # initial_capital
    try:
        initial_capital = kwargs['initial_capital']
    except KeyError as e:
        initial_capital = 100

    # N
    try:
        N = kwargs['N']
    except KeyError as e:
        print e
        N = 1000

    # binomial_model
    try:
        binomial_model = kwargs['binomial_model']
    except KeyError as e:
        binomial_model = binom(1, 0.5)

    # odds
    try:
        odds = kwargs['odds']
    except KeyError as e:
        odds = 2

    cmigc_dict = {
        'initial_capital': initial_capital,
        'N': N,
        'binomial_model': binomial_model,
        'odds': odds
        }

    return cmigc_dict

def calculate_multiple_iterations_given_criteria(M, kwargs):
    '''
    '''
    cmigc_dict = unpack_cmigc_kwargs(kwargs)
    initial_capital = cmigc_dict['initial_capital']
    N = cmigc_dict['N']
    binomial_model = cmigc_dict['binomial_model']

    iteration_list = []
    for iteration in xrange(M):
        result_array = calculate_returns_after_N_periods(
            initial_capital=initial_capital,
            N=N,
            binomial_model=binomial_model)
        iteration_list.append(result_array)

    iteration_array = np.array(iteration_list)

    df = pd.DataFrame(iteration_array)

    return df
