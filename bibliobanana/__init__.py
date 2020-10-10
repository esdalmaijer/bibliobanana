# Part of bibliobanana, by Edwin Dalmaijer
# https://github.com/esdalmaijer/bibliobanana

__author__ = "Edwin Dalmaijer"
__version__ = "0.1.3"

import os
import copy

from .get import get_yearly_count
from .io import write_results_to_file, load_results_from_file
from .plot import plot_yearly_count


def compute_yearly_citations(search_term, start_date, end_date, \
    comparison_terms="banana", database="pubmed", exact_phrase=True, \
    pubmed_field="text", pause=1.0, verbose=False, save_to_file=None, \
    plot_to_file=None, figsize=(8.0,6.0), dpi=100.0):
    
    # Wrap the search and comparison terms in a list.
    if type(search_term) not in [tuple, list]:
        search_term = [search_term]
    if type(comparison_terms) not in [tuple, list]:
        comparison_terms = [comparison_terms]
    # Check if all terms are strings.
    for term in search_term + comparison_terms:
        if type(term) != str:
            raise Exception("Passed term {} is not a string, but {}".format( \
                term, type(term)))
            if term == "":
                raise Exception("Passed term cannot be an empty string.")
    
    # Construct the beginning of the result dict, with clarifications on which
    # terms is the target, which are comparisons, and what the range is.
    result_dict = {"_target":search_term, "_comparison":comparison_terms, \
        "_year_range":list(range(start_date, end_date+1))}

    # Count and store the yearly hits for each term.
    for i, term in enumerate(search_term + comparison_terms):
        # Count the number of hits for this term.
        num = get_yearly_count(term, start_date, end_date, \
            exact_phrase=exact_phrase, pubmed_field=pubmed_field, \
            pause=pause, verbose=verbose)
        # Store the result in the result dict.
        result_dict[term] = copy.deepcopy(num)
    
    # Write the results to file if requested.
    if save_to_file is not None:
        write_results_to_file(save_to_file, result_dict)
    
    # Plot the results if requested.
    if plot_to_file is not None:
        # Plot the results.
        fig, ax = plot_yearly_count(result_dict, figsize=figsize, dpi=dpi)
        # Attempt to auto-detect the file extension.
        name, ext = os.path.splitext(plot_to_file)
        if ext == "":
            plot_to_file += ".png"
        elif ext.lower()[1:] not in \
            list(fig.canvas.get_supported_filetypes().keys()):
            print("WARNING: Chosen file extension '{}' not ".format(ext) + \
                "supported; reverting to PNG")
        # Save to file.
        fig.savefig(plot_to_file)
    
    return result_dict
