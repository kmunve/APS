import numpy as np


def stats(arr):
    af = arr.flatten()

    box_bot = np.nanpercentile(af, 25.0)
    box_top = np.nanpercentile(af, 75.0)
    box_center = np.nanpercentile(af, 50.0)  # np.median(af)
    flier_low = np.nanpercentile(af, 0.0)  # np.min(af)
    flier_high = np.nanpercentile(af, 100.0)  # np.max(af)

    return flier_low, box_bot, box_center, box_top, flier_high


def describe(arr):
    flier_low, box_bot, box_center, box_top, flier_high = stats(arr)
    desc = "The array is of shape {0}\n" \
           "The median is {1:.2f}\n" \
           "The first and third quartiles are {2:.2f} and {3:.2f}\n" \
           "The minimum is {4:.2f} and the maximum is {5:.2f}.\n".format(arr.shape, box_center, box_bot, box_top, flier_low, flier_high)

    return desc

# def box_plot(arr):
#     flier_low, box_bot, box_center, box_top, flier_high = stats(arr)

