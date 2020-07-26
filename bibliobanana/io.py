# Part of bibliobanana, by Edwin Dalmaijer
# https://github.com/esdalmaijer/bibliobanana

import os


def write_results_to_file(file_path, result_dict):
    
    # Attempt to auto-detect the file extension to choose a separator.
    name, ext = os.path.splitext(file_path)
    if ext == "":
        file_path += ".csv"
        sep = ","
    elif ext == ".csv":
        sep = ","
    elif ext == ".tsv":
        sep = "\t"
    else:
        sep = ","
    # Open a new file, and write results.
    with open(file_path, "w") as f:
        # Write a header to file.
        header = ["year"] + result_dict["_target"] + result_dict["_comparison"]
        f.write(sep.join(map(str, header)))
        # Write a second header to clarify what each term is.
        term_header = ["year"] + \
            len(result_dict["_target"]) * ["target"] + \
            len(result_dict["_comparison"]) * ["comparison"]
        f.write("\n" + sep.join(map(str, term_header)))
        # Write all lines to file.
        for i, year in enumerate(result_dict["_year_range"]):
            line = [year]
            for term in result_dict["_target"] + result_dict["_comparison"]:
                line.append(result_dict[term][i])
            # Write this year's line to file.
            f.write("\n" + sep.join(map(str, line)))


def load_results_from_file(file_path, sep=None):
    
    if not os.path.isfile(file_path):
        raise Exception("Could not find file at path {}".format(file_path))

    # Attempt to auto-detect the file extension to choose a separator.
    if sep is None:
        name, ext = os.path.splitext(file_path)
        if ext == ".csv":
            sep = ","
        elif ext == ".tsv":
            sep = "\t"
        else:
            sep = ","
    
    # Start with an empty result dict.    
    result_dict = {}

    # Open the file, and extract its contents.
    with open(file_path, "r") as f:
        # Read all lines.
        lines = f.readlines()
    
    # Parse the headers.
    header = lines.pop(0).replace("\n", "").split(sep)
    term_header = lines.pop(0).replace("\n", "").split(sep)
    # Check which types of terms were recorded.
    if "year" not in term_header:
        raise Exception("Could not find the year column in the second header.")
    else:
        result_dict["_year_range"] = []
    for term_type in ["target", "comparison"]:
        if term_type in term_header:
            result_dict["_{}".format(term_type)] = []
    # Extract the terms.
    for i, term_type in enumerate(term_header):
        # Only extract target and comparison terms.
        if term_type in ["target", "comparison"]:
            # Add the term (from the header) to the correct list.
            result_dict["_{}".format(term_type)].append(header[i])
            # Create an empty entry for this term.
            result_dict[header[i]] = []

    # Parse the data.
    for i, line in enumerate(lines):
        # Throw away the trailing newline, and split by separator.
        line = line.replace("\n", "").split(sep)
        # Grab this line's year.
        year = line[term_header.index("year")]
        result_dict["_year_range"].append(int(year))
        # Grab the data for all terms.
        for term_type in ["target", "comparison"]:
            for term in result_dict["_{}".format(term_type)]:
                result_dict[term].append(int(line[header.index(term)]))
    
    return result_dict
        
