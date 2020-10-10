import os
from matplotlib import pyplot
from bibliobanana import compute_yearly_citations, load_results_from_file, \
    plot_yearly_count

# Define the search terms of interest.
search_terms = [ \
    "H1N1", \
    "H5N1", \
    "H7N9", \
    "H3N2", \
    "SARS-CoV-2", \
    ]

# Define the comperison terms.
comparison_terms = ["virus"]
# Define the search range.
start_date = 1969
end_date = 2020
# Construct the name of the file to which we should save the data.
save_file = "respiratory_{}-{}".format(start_date, end_date)

# Get the results from PubMed.
if not os.path.isfile(save_file+".csv"):
    print("Getting data from PubMed...")
    result = compute_yearly_citations(search_terms, start_date, end_date, \
        comparison_terms=comparison_terms, database="pubmed", \
        exact_phrase=True, pause=0.5, verbose=True, \
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
fig, ax = pyplot.subplots(nrows=2, ncols=1, sharex=True, figsize=(8.0,6.0), \
    dpi=600.0)
fig.subplots_adjust(left=0.11, right=0.99, bottom=0.13, top=0.99)
for a in ax:
    fig, a = plot_yearly_count(result, plot_ratio=True, \
        plot_average_comparison=False, scale_to_max=False, \
        ax=a, figsize=(8.0,6.0), dpi=600.0)
# Set the y limit of the bottom figure.
ax[1].set_ylim(0, 0.12)
#ax[0].set_ylim(0.30, 0.42)
ax[0].set_ylim(0.42, 0.54)
# Remove the legend from the bottom plot, and move the legend in the top plot
# to the top-left.
ax[0].legend(loc="upper left", fontsize=16)
ax[1].get_legend().remove()
# # Hide the spines between the axes.
ax[1].spines["top"].set_visible(False)
ax[0].spines["bottom"].set_visible(False)
ax[0].xaxis.tick_top()
ax[0].tick_params(labeltop=False)
ax[1].xaxis.tick_bottom()
# Remove the top ax y label, and shift the bottom y label up.
ax[0].set_ylabel("")
ax[1].yaxis.set_label_coords(-0.075, 1.1)
# Save the figure.
fig.savefig(save_file+"_ratios.png")

print("All done!")
