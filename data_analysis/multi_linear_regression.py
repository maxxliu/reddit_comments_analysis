# CS121 Linear regression
#
# Spencer Ho

import numpy as np
import pandas as pd
import random
import dataframe
#from asserts import assert_Xy, assert_Xbeta


# because Guido van Rossum hates functional programming
# http://www.artima.com/weblogs/viewpost.jsp?thread=98196
from functools import reduce

def the_command(df):
    df = dataframe.CREATE_DATAFRAME('FINAL_COMP.txt', 'TRAINING_DATA.csv', 'FINAL_COMP_SENT.txt', (3,4), (9,10),1)
    train_df, test_df, test_index_lst = create_trainer_dataframe(df)
    lin_dict = model(train_df, 'EPS', ['w9avg'], ['w9cnt'])
    s_rate = success_rate(test_df, lin_dict['beta'][0], test_index_lst, ['w9avg', 'w9cnt'], 'EPS')
    return s_rate, lin_dict['beta'][0], ['w9avg', 'w9cnt'], 'EPS', lin_dict['R_squared'] 

def create_trainer_dataframe(df):
    rand_lst = random.sample(range(90),90)
    point_index_lst = rand_lst[0:80]
    test_index_lst = rand_lst[80:90]
    frames = []
    for i in point_index_lst:
        frames.append(df.loc[[i]])
    train_df = pd.concat(frames)
    frames = []
    for j in test_index_lst:
        frames.append(df.loc[[j]])
    test_df = pd.concat(frames)
    return train_df, test_df, test_index_lst

def success_rate(test_df, beta_list, test_index_lst, pred_list, response_var):
    success_count = 0
    for i in test_index_lst:
        val = test_df[pred_list].loc[i].values
        pred_z = beta_list[0] + beta_list[1]*val[0] + beta_list[2]*val[1]
        act_z = test_df[[response_var]].loc[i].values
        act_z = act_z.astype(np.float)
        if (bool(act_z > 0) == bool(pred_z > 0)):
            success_count += 1
    return success_count






def model(df, response_var, predictors_list, predictor_variables, total=False):
    '''
    Inputs: trainer_data_set, dependent_variable_index, predictor_list, predictor_variables
    Outputs: a dictionary with beta, R_squared, for each additional predictor_variable added onto predictors_list
    and y_mean 
    Also has the option of creating a dictionary with beta, R_squared, and y_mean specific to predictors_list
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

def bivariate_model(X_o, y_orig, predictor_variables):
    '''
    compares all possible bivariate models and returns the two predictors that have highest R2 value
    Inputs: trainer data, dependent_variable_index, predictor_variables
    Output: A tuple with max rsquared value, first predictor, and second predictor respectively

    '''
    winner = (0, 0, 0)
    duplicater_check = predictor_variables
    for i in range(len(predictor_variables) - 1):
        p_model = {}
        p_model = model(X_o, y_orig, [i], duplicater_check)
        potential_winner = max(p_model["R_squared"])
        if potential_winner[0][0] > winner[0]:
           second_predictor = potential_winner[0][1]
           max_r_squared = potential_winner[0][0]
           winner = (max_r_squared, i, second_predictor)
        duplicater_check.pop(0)  
    return winner



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
    Inputs: trainer_data_set, dependent_variable_index, predictor_list, predictor_variables, column names, and threshold
    Outputs: list of best variables to create best model, respective R_squared list and beta_list
    threshold can limit total number of variables added to list
    '''
    beta_list = []
    predictors_list = []
    R2_list = []
    t = float('inf')
    past_R2 = 0
    predictor_variables = df.columns.values
    predictor_variables = predictor_variables[0:(len(predictor_variables)-1)]
    print(predictor_variables)
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
    Takes beta generated in trainer models and uses it to create new R_squared values with the new test data
    inputs: test data, test dependent_variable_index, trainer model's generated beta lists and predictors_list
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

def name_p_list(predictors_list, R2_list, col_names):
    '''
    Takes numerical representations of the best variable list and changes them to columns and finally prints data nicely
    inputs: predictors list, respective R_squared list, column names
    outputs: prints the predictors/ list of predictors and the respective R2
    '''
    predictors_list_n = []
    for  name  in predictors_list:
        predictors_list_n.append(col_names[name])
    for i in range(len(predictors_list_n)):
        predictors = (', ').join(predictors_list_n[: i + 1])
        print(("{} {}:{:.2f}").format(predictors, "R2", R2_list[i]))



def prepend_ones_column(A):
    '''
    Add a ones column to the left side of an array

    Inputs: 
        A: a numpy array

    Output: a numpy array
    '''
    ones_col = np.ones((A.shape[0], 1))
    return np.c_[ones_col, A]


def linear_regression(X, y):
    '''
    Compute linear regression. Finds model, beta, that minimizes
    X*beta - Y in a least squared sense.

    Accepts inputs with type array
    Returns beta, which is used only by apply_beta

    Examples
    --------
    >>> X = np.array([[5, 2], [3, 2], [6, 2.1], [7, 3]]) # predictors
    >>> y = np.array([5, 2, 6, 6]) # dependent
    >>> beta = linear_regression(X, y)  # compute the coefficients
    >>> beta
    array([ 1.20104895,  1.41083916, -1.6958042 ])
    >>> apply_beta(beta, X) # apply the function defined by beta
    array([ 4.86363636,  2.04195804,  6.1048951 ,  5.98951049])
    '''
    #assert_Xy(X, y, fname='linear_regression')

    X_with_ones = prepend_ones_column(X)

    # Do actual computation
    beta = np.linalg.lstsq(X_with_ones, y)[0]

    return beta



def apply_beta(beta, X):
    '''
    Apply beta, the function generated by linear_regression, to the
    specified values

    Inputs:
        model: beta as returned by linear_regression
        Xs: 2D array of floats

    Returns:
        result of applying beta to the data, as an array.

        Given:
            beta = array([B0, B1, B2,...BK])
            Xs = array([[x11, x12, ..., x0K],
                        [x21, x22, ..., x1K],
                        ...
                        [xN1, xN2, ..., xNK]])

            result will be:
            array([B0+B1*x11+B2*x12+...+BK*x1K,
                   B0+B1*x21+B2*x22+...+BK*x2K,
                   ...
                   B0+B1*xN1+B2*xN2+...+BK*xNK])
    '''
    #assert_Xbeta(X, beta, fname='apply_beta')

    # Add a column of ones
    X_incl_ones = prepend_ones_column(X)

    # Calculate X*beta
    yhat = np.dot(X_incl_ones, beta)
    return yhat


def read_file(filename):
    '''
    Read data from the specified file.  Split the lines and convert
    float strings into floats.  Assumes the first row contains labels
    for the columns.

    Inputs:
      filename: name of the file to be read

    Returns:
      (list of strings, 2D array)
    '''
    with open(filename) as f:
        labels = f.readline().strip().split(',')
        data = np.loadtxt(f, delimiter=',', dtype=np.float64)
        return labels, data



