from pandas import read_csv


def load_companies(country="DEU"):
    """
    Load dummy datasets for either Germany ("DEU") or Italy ("ITA"). These
    contain the name of the 100 companies with the largest estimated number of
    employees for each German state (NUTS 1) or each Italian region (NUTS 2).
    The data was obtained from the 2019 Global Company Dataset published
    publicly by People Data Labs.

    Parameters
    ----------
    country : str, optional (default = "DEU")
        If ```country = DEU```, loads German dataset. If ```country = ITA```,
        loads Italian dataset.

    Returns
    -------
    DataFrame
        The DataFrame corresponding to the chosen country.
    """
    df = read_csv(f"./data/companies_{country}.csv", encoding='utf-8')

    return df
