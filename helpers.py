def getfraction(position_in_capture, capture, screen):
    position_in_screen = (position_in_capture * screen) / capture
    return position_in_screen


def find_average(list):
    ncols = len(list[0])
    nrows = len(list)
    # Sum all elements in each column:
    results = ncols * [0]  # sums per column, afterwards avgs
    for col in range(ncols):
        for row in range(nrows):
            results[col] += list[row][col]
    # Then calculate averages:
    # * nrows is also number of elements in every col:
    num_of_elements = float(nrows)

    results = [int(sum / num_of_elements) for sum in results]
    return results


def map(value, start1, stop1, start2, stop2):
    newValue = ((value - start1) / (stop1 - start1)) * \
        (stop2 - start2) + start2
    return newValue
