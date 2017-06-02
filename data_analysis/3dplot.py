import numpy as np
import matplotlib.pyplot as plt
import random
from mpl_toolkits.mplot3d import Axes3D

def plotter_i_hardly_know_her(df, beta_list, exp_lst, result_var):
    max_v1 = max(df[exp_lst[0]].values)*10
    min_v1 = min(df[exp_lst[0]].values)*10
    max_v2 = max(df[exp_lst[1]].values)/1000
    min_v2 = min(df[exp_lst[1]].values)/1000
    points = df[[exp_lst[0], exp_lst[1]]]
    c, a, b = beta_list
    normal = np.array([(-a/c), (-b/c), (1/c)])
    point = np.array([0,0,c])
    # point_index_lst = []
    # for i in range(80):
    #     point_index_lst.append(random.randint(0,99))
    # point_index_lst.sort()
    # test_point_index = []
    
    d = -1
    x_lo_bound = int(min_v1 - min_v1*0.1)
    x_up_bound = int(max_v1 + max_v1*0.1)
    y_lo_bound = int(min_v2 - min_v2*0.1)
    y_up_bound = int(max_v2 + max_v2*0.1)
    xx, yy = np.mgrid[x_lo_bound:x_up_bound:30j, y_lo_bound:y_up_bound:30j]
    z1 = (-normal[0]*xx - normal[1]*yy - d)*1/normal[2]
    plt3d = plt.figure().gca(projection='3d')
    plt3d.plot_surface(xx,yy,z1, color='blue', alpha=0.5)
    ax = plt.gca()
    ax.hold(True)
    points = df[[exp_lst[0], exp_lst[1], result_var]].values
    points = points.astype(np.float)
    for point in points:
       ax.scatter(point[0]*10, point[1]/1000, point[2], s=10, color='green')
    ax.view_init(azim=30)
    ax.set_xlabel(exp_lst[0] + ' (1 x 10 ^-1)')
    ax.set_ylabel(exp_lst[1] + ' (in thousands)')
    ax.set_zlabel(result_var)
    plt.savefig('plot.pdf')
