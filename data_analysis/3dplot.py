import numpy as np
import matplotlib.pyplot as plt
import random
from mpl_toolkits.mplot3d import Axes3D

def three_d_plot(df, beta_list, exp_lst, result_var):
    '''
    Inputs: dataframe, a list of beta_scores,
    a list of explanatory variables (only two), the result variable.

    Outputs: A 3D graph
    '''
    max_v1 = max(df[exp_lst[0]].values)
    min_v1 = min(df[exp_lst[0]].values)
    max_v2 = max(df[exp_lst[1]].values)
    min_v2 = min(df[exp_lst[1]].values)
    xx, yy = np.mgrid[min_v1:max_v1:30j, min_v2:max_v2:30j]
    points = df[[exp_lst[0], exp_lst[1]]]
    c, a, b = beta_list
    normal = np.array([(-a/c), (-b/c), (1/c)])
    point = np.array([0,0,c])
    d = -1
    z = (-normal[0]*xx - normal[1]*yy - d)*1/(normal[2])

    #scales the graph to see results better
    if max_v1 > 1000:
        max_v1 = max_v1/1000
        min_v1 = min_v1/1000
        x_label = ' (in thousands)'
        x_factor = .001
    else:
        max_v1 = max_v1*10
        min_v1 = min_v1*10
        x_label = ' (1 x 10 ^-1)'
        x_factor = 10

    if max_v2 > 1000:
        max_v2 = max_v1/1000
        min_v2 = min_v1/1000
        y_label = ' (in thousands)'
        y_factor = .001
    else:
        max_v2 = max_v2*10
        min_v2 = min_v2*10
        y_label = ' (1 x 10 ^-1)'
        y_factor = 10

    points = df[[exp_lst[0], exp_lst[1]]]
    c, a, b = beta_list
    normal = np.array([(-a/c), (-b/c), (1/c)])
    point = np.array([0,0,c])
    d = -1
    x_lo_bound = int(min_v1 - min_v1*0.1)
    x_up_bound = int(max_v1 + max_v1*0.1)
    y_lo_bound = int(min_v2 - min_v2*0.1)
    y_up_bound = int(max_v2 + max_v2*0.1)
    xx_fit, yy_fit = np.mgrid[x_lo_bound:x_up_bound:30j, y_lo_bound:y_up_bound:30j]
    z1 = (-normal[0]*xx - normal[1]*yy - d)*1/(normal[2])
    plt3d = plt.figure().gca(projection='3d')
    plt3d.plot_surface(xx_fit,yy_fit,z, color='blue', alpha=0.5)
    ax = plt.gca()
    ax.hold(True)
    points = df[[exp_lst[0], exp_lst[1], result_var]].values
    points = points.astype(np.float)
    for point in points:
       ax.scatter(point[0]*x_factor, point[1]*y_factor, point[2], s=10, color='green')
    ax.view_init(azim=30)
    ax.set_xlabel(exp_lst[0] + x_label)
    ax.set_ylabel(exp_lst[1] + y_label)
    ax.set_zlabel(result_var)
    ax.set_title('3D Multi-Linear Regression Model')
    plt.savefig('3dplot.pdf')
    plt.close()

def residual_plot(df, beta_list, exp_lst, result_var):
    '''
    Inputs: dataframe, a list of beta_scores,
    a list of explanatory variables, the result variable.

    Outputs: A residual graph
    '''
    c, a, b = beta_list
    points = df[[exp_lst[0], exp_lst[1], result_var]].values
    points = points.astype(np.float)
    plt.plot([0,50], [0,0], 'k-')
    x = []
    dif_list = []
    for i in range(len(points)):
        z = c + a*(points[i][0]) + b*(points[i][1])
        difference = z - points[i][2]
        x.append(i)
        dif_list.append(difference)
    plt.plot(x, dif_list, 'o')
    plt.ylabel('Residuals')
    plt.xlabel('Companies')
    plt.title('Residual Plot')
    plt.savefig('residual_plot.pdf')
    plt.close()
