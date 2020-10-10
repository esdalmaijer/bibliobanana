import os
from bibliobanana import compute_yearly_citations, load_results_from_file, \
    plot_yearly_count

search_term = "increased interest"
start_date = 1964
end_date = 2020

save_file = "{}_{}-{}".format(search_term, start_date, end_date)

# Get the results from PubMed.
if not os.path.isfile(save_file+".csv"):
    result_dict = compute_yearly_citations(search_term, start_date, end_date, \
        comparison_terms="banana", database="pubmed", pause=0.5, verbose=True, \
        save_to_file=save_file+".csv", plot_to_file=None)
# Load the results from a local file.
else:
    result_dict = load_results_from_file(save_file+".csv")

# Plot the results.
fig, ax = plot_yearly_count(result_dict, plot_ratio=False, \
    plot_average_comparison=False, scale_to_max=False, \
    figsize=(8.0,6.0), dpi=600.0)
fig.savefig(save_file+".png")
