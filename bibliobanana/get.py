# Part of bibliobanana, by Edwin Dalmaijer
# https://github.com/esdalmaijer/bibliobanana

from bs4 import BeautifulSoup
from urllib.request import Request, build_opener
import json, re, time, urllib

def get_num_results_scholar(search_term, start_date, end_date):
    """Helper method, sends HTTP request and returns response payload.
    
    Arguments
    
    search_term     -   str. Search term to count Google Scholar hits for.

    start_date      -   int. Year from which to count results for (inclusive).

    end_date        -   int. Year until which to count results for (inclusive).

    Returns
    
    num, success    -   [int, bool]. num gives the count of papers mentioning 
                        search_term for given range (start_date - end_date).
                        success == False when the search didn't retrun. In the
                        case of an Exception, the returned num will actually
                        be a str clarifying the error.
    """

    # This is based on a script by Volker Strobel, which was later improved by 
    # Patrick Hofmann. For the original, see:
    # https://github.com/Pold87/academic-keyword-occurrence
    #
    # Further changes made by Edwin Dalmaijer.

    # Open website and read html
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
    query_params = { \
        'q':        search_term, \
        'as_ylo':   start_date, \
        'as_yhi':   end_date, \
        }
    url = "https://scholar.google.com/scholar?as_vis=1&hl=en&as_sdt=1,5&" + \
        urllib.parse.urlencode(query_params)
    opener = build_opener()
    request = Request(url=url, headers={'User-Agent':user_agent})
    try:
        handler = opener.open(request)
    except Exception as e:
        return str(e), False
    html = handler.read() 

    # Create soup for parsing HTML and extracting the relevant information
    soup = BeautifulSoup(html, 'html.parser')
    # Find line 'About x results (y sec)
    div_results = soup.find("div", {"id": "gs_ab_md"})

    # Check if a result is returned.
    if div_results is None:
        success = False
        num_results = 0

    else:
        # Extract number of search results
        res = re.findall(r'(\d+).?(\d+)?.?(\d+)?\s', div_results.text)
        
        # If res is an empty string, the result is 0.
        if res == []:
            num_results = 0
            success = True
        # Convert the string to a number.
        else:
            num_results = int(''.join(res[0]))
            success = True

    return num_results, success


def get_num_results_pubmed(search_term, year, field="word"):
    
    # If you're reading this, thinking "What could I do to change the search
    # fields? The following are valid fields in Entrez:
    # [AFFL]    - Affiliation
    # [ALL]     - All Fields
    # [AUTH]    - Author
    # [FAUT]    - Author - First
    # [LAUT]    - Author - Last
    # [PDAT]    - Date - Publication
    # [FILT]    - Filter
    # [JOUR]    - Journal
    # [LANG]    - Language
    # [MAJR]    - MeSH Major Topic
    # [SUBH]    - MeSH Subheading
    # [MESH]    - MeSH Terms
    # [PTYP]    - Publication Type
    # [WORD]    - Text Word
    # [TITL]    - Title
    # [TIAB]    - Title/Abstract
    # [UID]     - UID

    # Make the search term URL-friendly.
    url_search_term = urllib.parse.quote(search_term)

    # Construct the query string.
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + \
        "db=pubmed&retmode=json&rettype=count&" + \
        "term={}[{}]+AND+{}[pdat]".format(url_search_term, field, year)
    
    # Make the search.
    opener = build_opener()
    request = Request(url=url)
    try:
        handler = opener.open(request)
    except Exception as e:
        return str(e), False
    json_str = handler.read()

    # Parse the result.
    json_dict = json.loads(json_str)
    num_results = 0
    success = False
    if "esearchresult" in json_dict.keys():
        if "count" in json_dict["esearchresult"].keys():
            num_results = int(json_dict["esearchresult"]["count"])
            success = True
    
    return num_results, success


def get_yearly_count(search_term, start_date, end_date, database="pubmed", \
    exact_phrase=True, pubmed_field="word", pause=1.0, verbose=False):
    
    """Returns a list with the yearly hit count for search_term from
    start_date until end_date (inclusive).

    Arguments
    
    search_term     -   str. Search term to count Google Scholar hits for.

    start_date      -   int. Year from which to count results for (inclusive).

    end_date        -   int. Year until which to count results for (inclusive).
    
    Keyword arguments
    
    database        -   str. Choose the database to query yearly counts from.
                        Currently available are:
                            "scholar" for Google Scholar
                            "pubmed" for pubmed
                        Please note that all databases come with specific rate
                        limits, which you should stay under to prevent getting
                        blocked. Google Scholar's limit seems particularly
                        low. PubMed's free limit is 3 queries per second.
    
    pause           -   float. Number of seconds to pause between each search
                        query. Increase to prevent over-querrying Google
                        Scholar, which might flag and block suspiciously fast
                        and/or numerous requests. Default = 1.0
    
    exact_phrase    -   bool. Set to True to see automatically add quotes to
                        your search query. This ensures you search for exact
                        matches with your query, e.g. "prefrontal cortex"
                        instead of "prefrontal" and/or "cortex".
                        Default = True
    
    verbose         -   bool. Set to True to see output printed to the console
                        with each year's count as it comes in. Default = False

    Returns
    
    result          -   list. The yearly count of papers mentioning "banana",
                        with len(result) == end_date - start_date.
    """
    
    # Add quotes if required.
    if exact_phrase:
        search_term = "\"{}\"".format(search_term)
    
    # Find the correct database.
    if database.lower() in ["google scholar", "googlescholar", "scholar", \
        "gscholar"]:
        database = "google scholar"
    elif database.lower() in ["pubmed", "ncbi", "pm", "medline"]:
        database = "pubmed"
    
    # Optionally report the start.
    if verbose:
        print("Searching for '{}' from {} until {}".format(search_term, \
            start_date, end_date))

    # Create an empty list to store results in.
    result = []
    # Loop through all dates (inclusive).
    for date in range(start_date, end_date + 1):
        # Google Scholar
        if database == "google scholar":
            # Count the number of search results for this year.
            num_result, success = get_num_results_scholar(search_term, date, \
                date)
        # PubMed
        elif database == "pubmed":
            # Count the number of search results for this year.
            num_result, success = get_num_results_pubmed(search_term, date, \
                field=pubmed_field)
        
        # Handle any exceptions.
        if not(success):
            if type(num_result) == str:
                raise Exception(num_result)
            else:
                raise Exception("Could not make a request to " + \
                    "{}".format(database) + \
                    ", or could not parse the request. This is an unknown " + \
                    "error. Sorry!")
        # Add the number to the result dict.
        else:
            result.append(num_result)

        # Optionally report the search results,
        if verbose:
            print("\t{}: {}".format(date, num_result))

        # Sleep to prevent over-asking and consequently being blocked, wait
        # for a bit until we run the next query.
        time.sleep(pause)
        
    return result
