import os
from bibliobanana import compute_yearly_citations, load_results_from_file, \
    plot_yearly_count

# MeSH terms of interest:
# Endocrine Gland Neoplasms [C04.588.322]
#    Adrenal Gland Neoplasms [C04.588.322.078]
#    Multiple Endocrine Neoplasia [C04.588.322.400]
#    Ovarian Neoplasms [C04.588.322.455]
#    Pancreatic Neoplasms [C04.588.322.475]
#    Paraneoplastic Endocrine Syndromes [C04.588.322.490]
#    Parathyroid Neoplasms [C04.588.322.525]
#    Pituitary Neoplasms [C04.588.322.609]
#    Testicular Neoplasms [C04.588.322.762]
#    Thyroid Neoplasms [C04.588.322.894]

# Define the search terms of interest.
search_terms = [ \
    "Adrenal Gland Neoplasms", \
    "Ovarian Neoplasms", \
    "Pancreatic Neoplasms", \
    "Pituitary Neoplasms", \
    "Testicular Neoplasms", \
    "Thyroid Neoplasms", \
    ]

# Define the comperison terms.
comparison_terms = ["Endocrine Gland Neoplasms"]
# Define the search range.
start_date = 1945
end_date = 2019
# Construct the name of the file to which we should save the data.
save_file = "MeSH-neoplasms_{}-{}".format(start_date, end_date)

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
