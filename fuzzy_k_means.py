import numpy as np
import math
from matplotlib import pyplot as plt
from numba import jit
import numba
from numba.typed import List
from decimal import Decimal



@jit(nopython=True)
def diff_stop(A, B):
    return np.sqrt(np.power((A - B),2)).sum()


def diff_stop_lists(A, B):
    total_sum = 0
    for i in range(len(A)):
        for j in range(len(A[0])):
            total_sum+= math.sqrt((A[i][j] - B[i][j])**2)
    return total_sum

@jit(nopython=True)
def norm(a, b):
    return np.linalg.norm(a-b)

def euclidean_distance(A, B):
    total_sum = 0
    for i in range(len(A)):
        total_sum+= (A[i] - B[i])**2
    return math.sqrt(total_sum)



@jit(nopython=True)
def fuzzy_k_means(epsilon, X, nb_clusters, m=1):
    # Initialize U Matrix
    U = np.random.rand(X.shape[0], nb_clusters)
    old_U = np.zeros((X.shape[0], nb_clusters))
    if len(X.shape) == 1:
        C = np.zeros((nb_clusters, 1))
    else:
        C = np.zeros((nb_clusters, X.shape[-1]))
    it=0
    while True:
        old_U = U.copy()

        # Calculate the center vectors
        for j in range(0, len(C)):
            # sum u_ij x_i
            sum_u_ij_x_i = np.zeros(C.shape[1:])
            # sum u_ij x_i
            sum_u_ij = np.zeros(C.shape[1:])
            for i in range(0, len(X)):
                #print(U[i, j]**m * X[i])
                sum_u_ij_x_i += U[i, j]**m * X[i]
                sum_u_ij += U[i, j]**m

            C[j] = sum_u_ij_x_i / sum_u_ij
            #print(C[j])

        # Update U
        for i in range(0, X.shape[0]):
            for j in range(0, C.shape[0]):

                # sum_clusters
                sum_divisor = 0
                for k in range(0, C.shape[0]):
                    x_i_c_j = norm(X[i], C[j])
                    x_i_c_k = norm(X[i], C[k])
                    try:
                        sum_divisor+= (x_i_c_j / x_i_c_k)**round(2/(m-1))
                    except:
                        print('x_i_c_j', x_i_c_j)
                        print('x_i_c_k', x_i_c_k)
                        print('(2/(m-1))', (2/(m-1)))
                        raise Exception

                U[i, j] = 1 / sum_divisor

        it+=1
        if (diff_stop(old_U, U) < epsilon):
            break
    return U

import random
import copy

def fuzzy_k_means_lists(epsilon, X, nb_clusters, m=1):
    # Declare U
    U = list()
    old_U = list()
    # Initialize U with random numbers and old_U with zeros
    for i in range(X.shape[0]):
        U.append([])
        old_U.append([])
        for j in range(nb_clusters):
            U[i].append(np.random.rand())
            old_U[i].append(0)
    U = np.random.rand(X.shape[0], nb_clusters)
    old_U = np.zeros((X.shape[0], nb_clusters))
    if len(X.shape) == 1:
        C = np.zeros((nb_clusters, 1))
    else:
        C = np.zeros((nb_clusters, X.shape[-1]))
    it=0
    while True:
        old_U = U.copy()
        # Calculate the center vectors
        for j in range(0, len(C)):
            # sum u_ij x_i
            sum_u_ij_x_i = np.zeros(C.shape[1:])
            # sum u_ij x_i
            sum_u_ij = np.zeros(C.shape[1:])
            for i in range(0, len(X)):
                #print(U[i, j]**m * X[i])
                sum_u_ij_x_i += U[i][j]**m * X[i]
                sum_u_ij += U[i][j]**m

            C[j] = sum_u_ij_x_i / sum_u_ij

        # Update U
        for i in range(0, X.shape[0]):
            for j in range(0, C.shape[0]):

                # sum_clusters
                sum_divisor = np.float64(0)
                for k in range(0, C.shape[0]):
                    x_i_c_j = norm(X[i], C[j])
                    x_i_c_k = norm(X[i], C[k])
                    sum_divisor+= (x_i_c_j / x_i_c_k)**(2/(m-1))
                    #print((2/(m-1)))

                U[i][j] = 1 / sum_divisor
        it+=1
        if (diff_stop_lists(np.array(old_U), np.array(U)) < epsilon):
            break
    return U

#fuzzy_k_means_lists(0.5, np.array([1,5,6,7,8,7, 5,3,12,16,0,12, 4]), 2, m=1.5)
