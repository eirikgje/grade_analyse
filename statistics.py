import numpy as np
import matplotlib.pyplot as plt
from utils import sort_grades
from grades import Grades

def plot_grade_histogram(ingrades, column=-1, **kwargs):
    plt.hist(ingrades.data[:, column], **kwargs)

def find_quantile(ingrades, quantile, column=-1, is_sorted=False):
    """Finds the top quantile.
    
    Rounds up, so that if you ask for the top ten percent, you might get the
    top eleven, not the top nine."""

    if not is_sorted:
        sorted_grades = utils.sort_grades(ingrades, column)
    else:
        sorted_grades = ingrades

    numgrades = sorted_grades.data.shape[0]
    num_in_quantile = np.int(np.ceil(numgrades * quantile))
    return (sorted_grades.data[numgrades - num_in_quantile, column]) 

def get_letter_grades(ingrades, letter_quantiles, column=-1, is_sorted=False):
    """Given grades and a dictionary of letters:quantiles, returns letter grades."""
    if not is_sorted:
        sorted_grades = utils.sort_grades(ingrades, column)
    else:
        sorted_grades = ingrades

    outdict = {}
    for letter, quantile in letter_quantiles.iteritems():
        outdict[letter] = find_quantile(sorted_grades, quantile, column=column, is_sorted=True)

    return outdict
