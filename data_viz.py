import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg')


def boxplot(L, out_file_name="boxplot.png",
            names=None, x_label="", y_label="", title=""):
    """
    constructs a boxplot and writes the plot to the specified filename
    Arguments
    ---------
    L : list of lists
        list of lists of numbers that will be put into a boxplot
    """
    if L is None:
        raise TypeError("boxplot : Please supply a list and")

    if not isinstance(L, (list, np.ndarray)):
        raise TypeError("boxplot : Incorrect input type, "
                        + "please supply a list!")

    if len(L) == 0:
        raise IndexError("boxplot : Unpopulated list!")

    list_types = [not isinstance(val, list)
                  for val in L]

    if any(list_types):
        raise TypeError("boxplot : List contains invalid type!")

    if type(out_file_name) != str:
        raise TypeError("boxplot : filename is invalid type!")

    else:
        fig = plt.figure(figsize=(3, 3), dpi=300)
        ax = fig.add_subplot(1, 1, 1)
        ax.title.set_text(title)
        ax.set_ylabel(y_label)
        ax.set_xlabel(x_label)

        ax.boxplot(L)
        plt.xticks(list(range(1, len(names)+1)), names)

    try:
        plt.savefig(out_file_name, bbox_inches='tight')
    except PermissionError:
        raise PermissionError(
            "boxplot : Unable to write to "+out_file_name +
            ". Check file permissions!")
    except ValueError:
        raise ValueError(
            "boxplot : Incompatible file extension on "+out_file_name)
