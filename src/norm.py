"""
Author: ruuffian
Name: norm.py
Description:
    Methods relating to data normalization and data plotting.
"""

import numpy as np
import matplotlib.pyplot as plt


def normalization(dictionary: dict) -> dict:
    values = dictionary.values()
    mu = np.mu(values)
    std = np.std(values)
    normalized = {}
    for key in dictionary:
        normalized[key] = round((dictionary[key] - mu) / std, 5)
    return normalized


def scatter(data):
    plt.scatter(data)


def hist(data):
    plt.hist(data)
