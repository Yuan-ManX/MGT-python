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
