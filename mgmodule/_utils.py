def mg_progressbar(iteration, total, prefix='', suffix='', decimals=1, length=40, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar.

    Parameters:
    -----------
    - iteration   - Required  : current iteration (Int)
    - total       - Required  : total iterations (Int)
    - prefix      - Optional  : prefix string (Str)
    - suffix      - Optional  : suffix string (Str)
    - decimals    - Optional  : positive number of decimals in percent complete (Int)
    - length      - Optional  : character length of bar (Int)
    - fill        - Optional  : bar fill character (Str)
    - printEnd    - Optional  : end character (e.g. "\\r", "\\r\\n") (Str)
    """
    import sys

    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    sys.stdout.flush()
    sys.stdout.write('\r%s |%s| %s%% %s' %
                     (prefix, bar, percent, suffix))
    # Print New Line on Complete
    if iteration == total:
        print()


def scale_num(val, in_low, in_high, out_low, out_high):
    """Scale a number linearly."""
    return ((val - in_low) * (out_high - out_low)) / (in_high - in_low) + out_low


def scale_array(array, new_min, new_max):
    """Scale an arrary linearly."""
    minimum, maximum = np.min(array), np.max(array)
    m = (new_max - new_min) / (maximum - minimum)
    b = new_min - m * minimum
    return m * array + b
