# Part of bibliobanana, by Edwin Dalmaijer
# https://github.com/esdalmaijer/bibliobanana

import numpy
from matplotlib import pyplot

# Colours are from the Tango Desktop Project's palette.
# In order of appearance: blue, green, purple, red, orange, brown
# Yellow is used as the comparison colour.
_colours = ["#204a87", "#4e9a06", "#5c3566", "#a40000", "#ce5c00", "#8f5902"]
_colour_for_comparison = "#c4a000"

def plot_yearly_count(result_dict, plot_ratio=False, \
    plot_average_comparison=True, scale_to_max=False, \
    ax=None, figsize=(8.0,6.0), dpi=100.0):
    
    """Plots the results from a result_dict.
    """
    
    # Create a new figure.
    if ax is None:
        fig, ax = pyplot.subplots(figsize=figsize, dpi=dpi)
        fig.subplots_adjust(left=0.11, right=0.99, bottom=0.13, top=0.99)
    else:
        fig = ax.get_figure()
    # We'll be keeping track of the maximum result (to scale the y axis), so
    # we start at 0. (It will be updated as we go along.)
    max_result = 0
    
    # If there are more than one comparison terms, compute their average.
    if len(result_dict["_comparison"]) > 1:
        # Collect all numbers in a single matrix, as float rather than int
        # to make sure we can average OK.
        shape = ( \
            len(result_dict["_comparison"]), \
            len(result_dict["_year_range"]))
        a = numpy.zeros(shape, dtype=numpy.float64)
        for i, term in enumerate(result_dict["_comparison"]):
            a[i,:] = numpy.array(result_dict[term], dtype=numpy.float64)
            if scale_to_max:
                a[i,:] /= numpy.max(a[i,:])
        # Compute average and 95% confidence intervals.
        m = numpy.mean(a, axis=0)
        # Only compute the following if more than two comparison terms are
        # available.
        if len(result_dict["_comparison"]) > 2:
            sd = numpy.std(a, axis=0)
            sem = sd / numpy.sqrt(a.shape[0]-1)
            ci = 1.96 * sem
        else:
            ci = None
    # If there is only one comparison term, use it.
    else:
        m = numpy.array(result_dict[result_dict["_comparison"][0]], \
            dtype=numpy.float64)
        if scale_to_max and numpy.max(m) > 0:
            m /= numpy.max(m)
        ci = None

    # Plot the results together if the user opted for this.
    if plot_average_comparison and not plot_ratio:
        # Choose the label for the line.
        if len(result_dict["_comparison"]) > 1:
            lbl = "comparison"
        else:
            lbl = result_dict["_comparison"][0]
        # Plot the average and confidence intervals.
        ax.plot(result_dict["_year_range"], m, "-", lw=2, \
            color=_colour_for_comparison, label=lbl)
        highest = numpy.max(m)
        if ci is not None:
            ax.fill_between(result_dict["_year_range"], m, m-ci, m+ci, \
                color=_colour_for_comparison, alpha=0.3)
            highest = numpy.max(m+ci)
        # Check if this term's maximum is higher than the mean plus the
        # confidence interval.
        if highest > max_result:
            max_result = highest
    # Plot the comparison results individually if the user opted for this.
    elif not plot_average_comparison and not plot_ratio:
        # Plot the results.
        for term in result_dict["_comparison"]:
            y = numpy.array(result_dict[term], dtype=numpy.float64)
            if scale_to_max and numpy.max(y) > 0:
                y /= numpy.max(y)
            ax.plot(result_dict["_year_range"], y, "-", lw=2, \
                color=_colour_for_comparison, label=term)
        # Check if this term's maximum is higher than the current.
        if numpy.max(y) > max_result:
            max_result = numpy.max(y)
    
    # Plot the results for all target terms.
    for i, term in enumerate(result_dict["_target"]):
        # Pick the next colour in the list.
        col = _colours[i % len(_colours)]
        # Overwrite the plot colour if there is no comparison, and the term
        # happens to be banana. This, obviously, turns the colour to yellow.
        if plot_ratio and term in ["banana","\"banana\"","\'banana\'"]:
            col = "#c4a000"
        # Compute the result.
        y = numpy.array(result_dict[term], dtype=numpy.float64)
        if scale_to_max and numpy.max(y) > 0:
            y /= numpy.max(y)
        if plot_ratio:
            y[m>0] /= m[m>0]
            # If the reference keyword is 0, comparisons make no sense. The
            # expected behaviour here could perhaps be to set the keyword
            # ratio to infinite, but given the futility of such a comparison,
            # perhaps NaN or 0 are better options.
            y[m==0] = numpy.NaN
        # Plot the line for the result.
        ax.plot(result_dict["_year_range"], y, "-", lw=2, color=col, \
            label=term)
        # Check if this term's maximum is higher than the current.
        if numpy.nanmax(y) > max_result:
            max_result = numpy.nanmax(y)
        
    # If we have more than 10 years, only write ticks on the even years.
    if 30 >= len(result_dict["_year_range"]) > 10:
        # The starting index (si) should be 0 if the first year is even, and
        # 1 if the first year is odd.
        si = result_dict["_year_range"][0] % 2
        # Create a list of indices to slice only the even years.
        xi = range(si, len(result_dict["_year_range"]), 2)
        # Create empty tick labels for all recorded years. (Note: This will
        # only work for years -999 to 9999; just up the number in "|U4" if
        # you're somehow still using this in the future, or want to include
        # references earlier than 999 BC.
        xticklabels = numpy.zeros(len(result_dict["_year_range"]), dtype="|U4")
        xticklabels[xticklabels=="0"] = ""
        # Set only the recorded year tick labels.
        xticklabels[xi] = numpy.array(result_dict["_year_range"])[xi]
    # If we have more than 30 years, only write ticks every 5 years.
    elif len(result_dict["_year_range"]) > 30:
        # Find the lowest year that is divisible by 5.
        si = None
        for i in range(len(result_dict["_year_range"])):
            if result_dict["_year_range"][i] % 5 == 0:
                si = i
                break
        # Create a list of indices to slice only the %5 years.
        xi = range(si, len(result_dict["_year_range"]), 5)
        # Create empty tick labels for all recorded years. (Note: This will
        # only work for years -999 to 9999; just up the number in "|U4" if
        # you're somehow still using this in the future, or want to include
        # references earlier than 999 BC.
        xticklabels = numpy.zeros(len(result_dict["_year_range"]), dtype="|U4")
        xticklabels[xticklabels=="0"] = ""
        # Set only the recorded year tick labels.
        xticklabels[xi] = numpy.array(result_dict["_year_range"])[xi]
    # If we have 10 years or fewer, simply use all as tick labels.
    else:
        xticklabels = map(str, result_dict["_year_range"])
    # Set the x ticks (for all recorded years) and x tick labels (created
    # above; either for all years or only for even years.)
    ax.set_xticks(result_dict["_year_range"])
    ax.set_xticklabels(map(str, xticklabels), fontsize=16, rotation=85)
    # Set the axis limits. For the x-axis, this is the first year minus 1,
    # and the last year plus one. For the y-axis, this is 0 to the maximum
    # number of search results plus a small margin.
    ax.set_xlim([result_dict["_year_range"][0]-1, \
        result_dict["_year_range"][-1]+1])
    ax.set_ylim([0, max_result*1.05])
    # Set the y label.
    if plot_ratio:
        if (len(result_dict["_comparison"]) == 1) and \
        (result_dict["_comparison"][0] in ["banana","\"banana\"","\'banana\'"]):
            ylbl = "Banana ratio"
        else:
            ylbl = "Relative publication ratio"
    else:
        ylbl = "Number of publications"
    if scale_to_max:
        ylbl += " (max-scaled)"
    ax.set_ylabel(ylbl, fontsize=20)
    # Draw the legend.
    ax.legend(loc="upper left", fontsize=16)
    
    return fig, ax
