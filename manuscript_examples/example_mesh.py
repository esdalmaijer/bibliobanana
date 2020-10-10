import os
from bibliobanana import compute_yearly_citations, load_results_from_file, \
    plot_yearly_count

# Define the search terms of interest.
search_terms = [ \
    "Denmark", \
    "Finland", \
    "Iceland", \
    "Norway", \
    "Sweden", \
    ]

# Define the comperison terms.
comparison_terms = ["Scandinavian and Nordic Countries"]
# Define the search range.
start_date = 1945
end_date = 2019
# Construct the name of the file to which we should save the data.
save_file = "MeSH-countries_{}-{}".format(start_date, end_date)

# Get the results from PubMed.
if not os.path.isfile(save_file+".csv"):
    print("Getting data from PubMed...")
    result = compute_yearly_citations(search_terms, start_date, end_date, \
        comparison_terms=comparison_terms, database="pubmed", \
        pubmed_field="mesh", exact_phrase=True, pause=0.5, verbose=True, \
        save_to_file=save_file+".csv", plot_to_file=None)
# Load from an existing file.
else:
    print("Loading data from file...")
    result = load_results_from_file(save_file+".csv")

print("Plotting results...")

# Plot the results.
fig, ax = plot_yearly_count(result, plot_ratio=False, \
    plot_average_comparison=False, scale_to_max=False, \
    figsize=(8.0,6.0), dpi=600.0)
fig.savefig(save_file+".png")

# Plot the results as ratios of the comparison terms.
fig, ax = plot_yearly_count(result, plot_ratio=True, \
    plot_average_comparison=False, scale_to_max=False, \
    figsize=(8.0,6.0), dpi=600.0)
# Remove the legend for this plot.
ax.get_legend().remove()
# Save the figure.
fig.savefig(save_file+"_ratios.png")

print("All done!")
