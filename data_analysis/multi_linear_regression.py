# CS121 Linear regression
#
# Spencer Ho

import numpy as np
import pandas as pd
import random
import dataframe

def success_and_r2_avg(comp_list_txt, train_data_csv, sent_csv, num_predictors,total_times):
    '''
    Runs the command function x amount of times and finds the average
    success score and R^2 score

    Inputs: A textfile that has a list of companies, a csv file that has 
    companies and their EPS percentage, a csv file that has a company's 
    sentiment scores, number of explanatory variables, and number 
    of times we would like to run our tests.

    Outputs: The average success rate and average R^2 score
    '''
    s_list = []
    R2_list = []
    for run in range(total_times):
        df, s_rate, betas, pred_list, r2 = \
        the_command(comp_list_txt, train_data_csv, sent_csv, num_predictors)
        s_list.append(s_rate)
        R2_list.append(r2)
    return sum(s_list) / len(s_list), sum(R2_list) / len(R2_list)



def the_command(comp_list_txt, train_data_csv, sent_csv, num_predictors):
    '''
    takes in 3 files to build a dataframe, finds the x amount of predictors
    and makes a multi-linear regression model out of them.  Using this model,
    it tests to see if it can correctly predict if a company will beat earnings

    Inputs: A textfile that has a list of companies, a csv file that has 
    companies and their EPS percentage, a csv file that has a company's 
    sentiment scores, number of explanatory variables, and number 
    of times we would like to run our tests.

    Outputs: original dataframe, success rate, list of beta scores,
    a list of the predictor variables, and r2 score 
    '''
    df = dataframe.CREATE_DATAFRAME(comp_list_txt, \
        train_data_csv, sent_csv, (1,4), (1,10),1)
    train_df, test_df, test_index_lst = create_trainer_dataframe(df)
    pred_list, R2_list, beta_list = \
    model_fitting_helper(train_df, 'EPS', 0, num_predictors)
    s_rate = success_rate(test_df, beta_list[len(beta_list)-1], \
        test_index_lst, pred_list, 'EPS')
    return df, s_rate, beta_list[len(beta_list)-1], pred_list, R2_list[len(R2_list)-1]

def create_trainer_dataframe(df):
    '''
    A helper function that breaks up original dataframe
    Into a testing dataframe of 10 companies and a 
    trainer dataframe made up of the rest of the companies.

    Inputs: the original dataframe

    Outputs: A trainer dataframe, a testing dataframe,
    and the original dataframe indexes of all the 
    testing companies.
    '''

    comp_count = len(df)
    rand_lst = random.sample(range(comp_count),comp_count)
    point_index_lst = rand_lst[0:(comp_count-10)]
    test_index_lst = rand_lst[(comp_count-10):comp_count]
    frames = []
    for i in point_index_lst:
        frames.append(df.loc[[i]])
    train_df = pd.concat(frames)
    frames = []
    for j in test_index_lst:
        frames.append(df.loc[[j]])
    test_df = pd.concat(frames)
    return train_df, test_df, test_index_lst

def success_rate(test_df, beta_list, \
    test_index_lst, pred_list, response_var):
    '''
    A helper function that determines how well the
    multi-linear regression model can predict if a 
    test company can beat earnings.

    Inputs: A testing dataframe, a list of betas,
    the indexes of the testing companies, a list 
    of explanatory variables, and the observed variable.

    Outputs: A count of successful predictions (out of 10)
    '''

    success_count = 0
    for i in test_index_lst:
        val = test_df[pred_list].loc[i].values
        pred_z = beta_list[0]
        for j in range(len(beta_list)-1):
            pred_z += beta_list[j+1]*val[j] 
        act_z = test_df[[response_var]].loc[i].values
        act_z = act_z.astype(np.float)
        if (bool(act_z > 0) == bool(pred_z > 0)):
            success_count += 1
    return success_count

def model(df, response_var, predictors_list, predictor_variables, total=False):
    '''
    Inputs: trainer_data_set, dependent_variable_index, 
    predictor_list, predictor_variables
    Outputs: a dictionary with beta, R_squared, 
    for each additional predictor_variable added onto predictors_list
    and y_mean 
    Also has the option of creating a dictionary with beta, R_squared, 
    and y_mean specific to predictors_list
    To be used as trainer model, beta values are recycled for test data
    '''
    model = {}
    model["beta"] = []
    model["R_squared"] = []
    model["predict_index"] = []
    y = df[response_var].values
    y = y.astype(np.float)


    y_mean = y.mean()
    model["y_mean"] = y_mean
    if total == False:
        for p in predictor_variables:
            if p not in predictors_list:
                beta = linear_regression(df[predictors_list + [p]].values, y)
                yhat = apply_beta(beta, df[predictors_list + [p]].values)
                model["beta"].append(beta)
                model["R_squared"].append(R_squared(y, yhat, y_mean))
                model["predict_index"].append(p)             
    else:
        beta = linear_regression(df[predictors_list], y)
        yhat = apply_beta(beta, df[predictors_list])
        model["beta"].append(beta)
        model["R_squared"].append(R_squared(y, yhat, y_mean))
        model["predict_index"].append(p)                     

    return model

def R_squared(y, yhat, y_mean):
    '''
    Calculates R_squared, is a helper function for model 
    Inputs: y, yhat, y_mean
    Outputs: R_squared
    '''
    top = ((y - yhat) ** 2).sum()
    bottom = ((y - y_mean) ** 2).sum()
    return 1 - (top / bottom) 

def model_fitting_helper(df, response_var, threshold, num_var_thresh): 
    '''
    Finds which variables generate the best model
    Inputs: trainer_data_set, dependent_variable_index, predictor_list,
     predictor_variables, column names, and threshold
    Outputs: list of best variables to create best model, 
    respective R_squared list and beta_list
    threshold can limit total number of variables added to list
    '''
    beta_list = []
    predictors_list = []
    R2_list = []
    t = float('inf')
    past_R2 = 0
    predictor_variables = df.columns.values
    predictor_variables = predictor_variables[0:(len(predictor_variables)-1)]
    while t > threshold and len(predictors_list) < num_var_thresh:
        beta_index = 0
        R2_best = 0
        p_model = {}
        p_model = model(df, response_var, predictors_list, predictor_variables)  
        for i in range(len(p_model["R_squared"])):
            if p_model["R_squared"][i] > R2_best:
                R2_best = p_model["R_squared"][i]
        t = R2_best - past_R2
        if t > threshold:
            predictors_list.append(p_model["predict_index"][i])
            past_R2 = R2_best
            R2_list.append(past_R2)
            beta_list.append(p_model["beta"][i])
    return predictors_list, R2_list, beta_list

def test_r_squared(X_test, y_test, beta_list, predictors_list):
    '''
    Takes beta generated in trainer models and uses it 
    to create new R_squared values with the new test data
    inputs: test data, test dependent_variable_index, trainer model's generated 
    beta lists and predictors_list
    outputs: a list of R_squared values using the new data
    '''
    test_r2 = []
    y = X_test[:, y_test]
    y_mean = y.mean()
    for i in range(len(predictors_list)):
        a = []
        a = predictors_list[:i + 1]
        yhat = apply_beta(beta_list[i], X_test[:, a])
        r_squared = R_squared(y, yhat, y_mean)
        test_r2.append(r_squared)
    return test_r2 


def add_ones_column(A):
    '''
    Adds a ones column to the left side of an array

    Inputs: 
        A: an array

    Output: an array with a ones column.
    '''
    ones_col = np.ones((A.shape[0], 1))
    return np.c_[ones_col, A]


def linear_regression(X, y):
    '''
    Computes a multi-linear regression. Finds the beta of 
    a least squared model.

    Input: An array of predictors and an array of explanatory variables

    Outputs: beta of a least squared model.
    '''
    X_plus_ones = add_ones_column(X)
    beta = np.linalg.lstsq(X_plus_ones, y)[0]

    return beta



def apply_beta(beta, X):
    '''
    Takes in a beta and an array of explanatory variables 
    and generates the predicted observed values.

    Inputs: Beta and an array of explanatory variables

    Outputs: The predicted observed values
    '''

    # Add a column of ones
    X_incl_ones = add_ones_column(X)

    # Calculate X*beta
    yhat = np.dot(X_incl_ones, beta)
    return yhat






