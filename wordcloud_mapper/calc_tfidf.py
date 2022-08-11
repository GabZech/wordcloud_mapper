import numpy as np

def calc_tfidf(df, nuts_codes, words, word_counts):
    """
    Calculates the Term Frequency — Inverse Document Frequency (TF-IDF) score
    for each word in each region present in the dataframe and returns a
    dataframe with three extra columns containing the TF, IDF and TF-IDF values
    for each word.
    To produce accurate results, please only include regions of the same
    hierarchical level in the input dataframe.
    Explanation of the TF-IDF score: If a word appears very often in a region
    and does not do so in other regions, then that word receives a high tf-idf
    score.
    Conversely, if a word appears very often in a region but also does so in
    many other regions, then that word receives a low tf-idf score.
    Therefore, the tf-idf score here is a measure of how relevant or unique a
    word is to that particular region in comparison to other regions.

    Parameters
    ----------
    df : DataFrame
        DataFrame containing columns with NUTS codes, words and word counts.
    nuts_codes : str
        Name of the column in the DataFrame containing the NUTS codes.
    words : str
        Name of the column in the DataFrame containing the words.
    word_counts : str
        Name of the column in the DataFrame containing the word counts.

    Returns
    -------
    DataFrame
        The same DataFrame as the input with three extra columns containing the
        TF, IDF and TF-IDF values for each word.
    """

    # calculate total count of words in each region
    total_counts_region = df.groupby([nuts_codes], as_index=False).sum()
    total_counts_region = total_counts_region\
        .rename(columns={word_counts: "total_counts_region"})
    df = df.merge(total_counts_region, how="left", on=nuts_codes)

    # calculate term frequency for each word in each region
    df["tf"] = df[word_counts] / df["total_counts_region"]

    # calculate total number of regions
    n_regions = len(df[nuts_codes].unique())

    # calculate number of regions containing each word
    word_occurrence = df[words].value_counts().rename_axis(words)\
        .reset_index(name='word_occurrence')
    df = df.merge(word_occurrence, how="left", on=words)

    # calculate inverse document frequency
    df["idf"] = np.log(n_regions / df["word_occurrence"])

    # calculate tf-idf
    df["tf-idf"] = df["tf"] * df["idf"]

    # remove NAs and normalise values to prevent errors related to font size
    # when generating the worldcloud
    df = df[df[words].notna()]
    df = df[df[word_counts].notna()]
    df["tf-idf"] = (df["tf-idf"]-df["tf-idf"].min())\
        /(df["tf-idf"].max()-df["tf-idf"].min())
    df = df[df["tf-idf"].notna()]

    # drop unnecessary columns
    df.drop(columns=["word_occurrence", "total_counts_region"], inplace=True)

    return df
