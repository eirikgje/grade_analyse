import numpy as np
from grades import Grades

def read_data(fname, mode, **kwargs):
    #This is a totally ad-hoc function. Mode currently 
    #is either 'eirik' or 'oystein', referring to which way the file is 
    #formatted
    if mode == "eirik":
        data=np.loadtxt(fname, skiprows=1, delimiter=',')
        data = np.append(data[:119, :], data[120:, :], axis=0)
        grade_data = Grades(data, mode="complete")
    elif mode == "oystein":
        grade_data = Grades(np.loadtxt(fname), mode="final_only")

    if "add_commands" in kwargs:
        comm_list = kwargs["add_commands"]
    else:
        comm_list = []
    if "remove_fail" in comm_list:
        grade_data = remove_fails(grade_data, kwargs["fail_filename"], kwargs["fail_delimiter"])
    if "sort_grades" in comm_list:
        if "sort_along_column" in kwargs:
            grade_data = sort_grades(grade_data, kwargs["sort_along_column"])
        else:
            grade_data = sort_grades(grade_data)

    return grade_data

def read_fails(fname, delimiter=','):
    """For the cases where the fails have been predetermined"""

    return np.loadtxt(fname, delimiter=delimiter)

def remove_entries_from_grades(ingrades, entries):
    rows = np.empty(0)
    for entry in entries:
        rows = np.append(rows, np.argwhere(ingrades.data[:, 0].astype(int) == entry))
    return Grades(np.delete(ingrades.data, rows, axis=0), mode=ingrades.mode)

def remove_fails(ingrades, fname, delimiter=','):
    fails = read_fails(fname, delimiter)
    return remove_entries_from_grades(ingrades, fails)

def sort_grades(ingrades, along_column=-1):
    return Grades(ingrades.data[ingrades.data[:, along_column].argsort()], mode=ingrades.mode)

def average_grades(ingrades, along_column=-1, round_nearest=True):
    """Along_column can be a list as well, if you want to average over two different columns"""

    #Test whether along_column is an iterable
    try:
        iterator = iter(along_column)
    except TypeError:
        along_column = np.array([along_column] * len(ingrades))
    else:
        along_column = np.array(along_column)
    if round_nearest:
        data = np.rint(np.array(ingrades[0].data[:, along_column[0]]))
    else:
        data = np.array(ingrades[0].data[:, along_column[0]])
    for i in xrange(1, len(ingrades)):
        if round_nearest:
            data += np.rint(ingrades[i].data[:, along_column[i]])
        else:
            data += ingrades[i].data[:, along_column[i]]
    data /= len(ingrades)

    return Grades(np.array([ingrades[0].data[:, 0], data]).T, mode="Averaged")
