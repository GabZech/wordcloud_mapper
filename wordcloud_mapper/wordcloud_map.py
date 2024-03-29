from shapefile import Reader
from numpy import unique, frombuffer, reshape, fromiter, uint8
import matplotlib.pyplot as plt
from descartes import PolygonPatch
from io import BytesIO
from wordcloud import WordCloud
from random import randint


def download_shapefiles(shapes_scale="10M",
                        nuts_year=2021,
                        coord_system=4326):
    """
    Download shapefiles for NUTS regions from Eurostat's GISCO database.

    Parameters
    ----------
    shapes_scale : str (default = "10M")
        Scale used for the regions' polygon shapes (i.e. regional boundaries).
        Smaller scales (e.g. "03M") mean more detailed polygon shapes and thus
        longer running times. Larger scales (e.g. "60M") mean less detailed
        polygon shapes and thus shorter running times. Available values:
        ``"60M"``, ``"20M"``, ``"10M"``, ``"03M"`` or ``"01M"``. For a visual
        explanation, see
        https://raw.githubusercontent.com/ropengov/giscoR/master/img/README-example-1.png
    nuts_year : int (default = 2021)
        The year of NUTS regulation, e.g. 2021, 2016, 2013, 2010, 2006 or 2003.
    coord_system : int (default = 4326)
        4-digit EPSG code (a unique identifier for different coordinate
        systems). Available values: ``4326`` (WGS84, coordinates in decimal
        degrees), ``3035`` (ETRS 1989 in Lambert Azimutal projection with
        centre in E52N10, coordinates in meters), ``3857`` (WGS84 Web Mercator
        Auxiliary Sphere, coordinates in meters).

    Returns
    -------
    shapefile.Reader
        Reader object of shapefile module containing shapefiles of NUTS
        regions.

    """
    url = f"https://gisco-services.ec.europa.eu/distribution/v2/nuts/shp/\
NUTS_RG_{shapes_scale}_{nuts_year}_{coord_system}.shp.zip"
    shapefiles = Reader(url)

    return shapefiles


def get_unique_codes(df,
                     nuts_codes):
    """
    Retrieve all unique NUTS codes in the provided dataset.

    Parameters
    ----------
    df : DataFrame
        DataFrame containing a column with NUTS codes.
    nuts_codes : str
        Name of the column in the DataFrame containing the NUTS codes.

    Returns
    -------
    unique_codes : ndarray
        Array containing unique NUTS codes.

    """
    unique_codes, counts = unique(df[nuts_codes].values, return_counts=True)

    return unique_codes


def get_bbox_map(shapefiles,
                 unique_codes):
    """
    Retreive the minimum and maximum X and Y bounding box values from all
    shapefiles to use as boundaries for the final wordcloud map.

    Parameters
    ----------
    shapefiles : shapefile.Reader
        Reader object of shapefile module containing shapefiles of NUTS
        regions.
    unique_codes : ndarray
        Array containing unique NUTS codes.

    Returns
    -------
    Xmin : float
        Minimum X value of bounding box.
    Ymin : float
        Minimum Y value of bounding box.
    Xmax : float
        Maximum X value of bounding box.
    Ymax : float
        Maximum Y value of bounding box.

    """
    # create lists with all bbox values
    Xmins = []
    Ymins = []
    Xmaxs = []
    Ymaxs = []

    for i, shaperecord in enumerate(shapefiles.shapeRecords()):
        nuts_id = shaperecord.record.NUTS_ID
        if nuts_id in unique_codes:
            minX, minY, maxX, maxY = shaperecord.shape.bbox
            Xmins.append(minX)
            Ymins.append(minY)
            Xmaxs.append(maxX)
            Ymaxs.append(maxY)

    # select only min and max values from lists
    Xmin, Ymin, Xmax, Ymax = min(Xmins), min(Ymins), max(Xmaxs), max(Ymaxs)

    return Xmin, Ymin, Xmax, Ymax


def get_bbox_region(shaperecord):
    """
    Retreive the minimum and maximum X and Y bounding box values for a given
    region.

    Parameters
    ----------
    shaperecord : shapefile.ShapeRecord
        ShapeRecord object of shapefile module containing information about a
        single NUTS region.

    Returns
    -------
    minX : float
        Minimum X value of bounding box.
    maxX : float
        Maximum X value of bounding box.
    minY : float
        Minimum Y value of bounding box.
    maxY : float
        Maximum X value of bounding box.

    """
    minX, minY, maxX, maxY = shaperecord.shape.bbox

    return minX, maxX, minY, maxY


def get_mask(shaperecord,
             fill_colour="black",
             contour_colour="black",
             resolution=100):
    """
    Create images to be used as mask (i.e. the shape) of the wordcloud and to
    add border lines to the final wordcloud map.

    Parameters
    ----------
    shaperecord : shapefile.ShapeRecord
        ShapeRecord object of shapefile module containing information about a
        single NUTS region.
    fill_colour : str (default = "black")
        Fill colour used when creating mask of region. Value None is passed
        when adding borders of regions to final wordcloud map.
    contour_colour : str (default = "black")
        Contour colour to use when showing regional borders in final wordcloud
        map.
    resolution : str (default = 100)
        DPI (dots per inch) value used to generate mask image. Higher values
        create sharper regional border lines but take longer to run.

    Returns
    -------
    img_arr : ndarray
        Array representing the image.

    """
    # create empty plot
    fig = plt.figure()
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    ax.margins(x=0, y=0, tight=True)
    fig.add_axes(ax)

    # plot region
    geometry = shaperecord.__geo_interface__["geometry"]
    if fill_colour is None:
        # used to plot region borders
        ax.add_patch(PolygonPatch(geometry, fill=False,
                     ec=contour_colour, alpha=0.3))
    else:
        ax.add_patch(PolygonPatch(
            geometry, fc=fill_colour, ec="black", alpha=1))

    # save image in memory buffer and reshape
    io_buf = BytesIO()
    fig.savefig(io_buf, format='raw', dpi=resolution, transparent=True)
    width, height = fig.get_size_inches() * resolution
    io_buf.seek(0)
    img_arr = frombuffer(io_buf.getvalue(), dtype=uint8)
    img_arr = reshape(img_arr, newshape=(int(height), int(width), -1))

    # close image and plot
    io_buf.close()
    plt.close(fig)

    return img_arr


def get_data(df,
             nuts_codes,
             words,
             word_counts,
             nuts_code,
             max_words
             ):
    """
    For a given NUTS code, retreive its words and their count/frequency from
    the DataFrame containing all data.

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
    nuts_code : str
        The NUTS code to filter on.
    max_words : int
        The number of words to plot on the wordcloud.

    Returns
    -------
    dict
        Dictionary containing the words as keys and their count as values for
        the given NUTS region.

    """
    # filter by nuts code, sort and select the top words
    df_temp = df.loc[df[nuts_codes] == nuts_code]\
                .dropna(subset=[words])\
                .sort_values(word_counts, ascending=False)\
                .head(max_words)
    dic = dict(zip(df_temp[words], df_temp[word_counts]))

    return dic


def plot_region(mask,
                data,
                ax,
                bbox,
                colour_func="random",
                colour_hue=None,
                rendering_quality=1,
                min_font_size=4,
                max_font_size=None,
                max_words=200,
                relative_scaling=0.5,
                prefer_horizontal=0.9,
                repeat=False):
    """
    Plot the wordcloud for a single region.

    Parameters
    ----------
    mask : ndarray
        The image array to use as mask (i.e. shape) of the wordcloud.
    data : dict
        Dictionary containing the words as keys and their count as values for
        the given NUTS region.
    ax : matplotlib.Axes class
        An instance of the matplotlib Axes class to which the wordcloud is
        plotted to.
    bbox : tuple
        Tuple containing (minX, maxX, minY, maxY) bounding box values of the
        region.
    colour_func : str (default = "random")
        String indicating which colour function to use. Available values:
        ``"random"`` sets a random luminosity to each word within a region,
        ``"frequency"`` sets the luminosity of each word according to their
        frequency/word count, where the most frequent word receives the max
        luminosity of 50,
         ``"rank"`` set the luminosity of each word according to their rank,
        where the word with rank=1 receives the max luminosity of 50.
    colour_hue : int or None (default = None)
        Sets one specific hue in the HSL colour system for all regions.
        Choose an integer between 0 and 360.
    rendering_quality : int (default = 1)
        The rendering quality of the words in the wordcloud. Higher values
        produce better-looking / sharper words but take longer to run.
    min_font_size : int (default = 4)
        Smallest font size to use. Word placement will stop when there is no
        more room to fit words of this size.
    max_font_size : int or None (default = None)
        Maximum font size for the largest word. If None, a relative sizing
        based on the height of the image is used.
    max_words : int (default = 200)
        Maximum number of words to be included in wordcloud for each region.
    relative_scaling : float (default = 'auto')
        Importance of relative word frequencies for font-size. With
        ``relative_scaling = 0``, only the ranking of words is considered. With
        ``relative_scaling = 1``, a word that is twice as frequent will have
        twice the size. In datasets with highly uneven word frequencies,
        relative_scaling = 1 might lead to very few words being fitted, so a
        value of around 0.5 often looks better. If ``relative_scaling =
        'auto'`` it will be set to 0.5 unless ``repeat = True``, in which case
        it will be set to 0.
    prefer_horizontal : float (default = 0.9)
        The ratio of times to try horizontal fitting as opposed to vertical. If
        ``prefer_horizontal = 1``, no words will be placed vertically. If
        ``prefer_horizontal < 1``, the algorithm will try rotating the word if
        it doesn't fit.
    repeat : bool (default = False)
        Whether to repeat already-placed words until ``max_words`` or
        ``min_font_size`` is reached.

    """
    # check colour_hue input
    if colour_hue == None:
        # set a random hue colour
        hue = randint(0, 360)
    elif 0 <= colour_hue <= 360:
        hue = colour_hue
    elif 0 < colour_hue > 360:
        print("Please choose an integer between 0 and 360")
        return

    def colour_func_random(word,
                           **kwargs):
        """
        Set a random luminosity to each word within a region.

        Parameters
        ----------
        word : str
            The word being plotted.

        Other Parameters
        ----------------
        **kwargs
            Keyword arguments passed to the colour function of the wordcloud.

        Returns
        -------
        str
            String containing HSL colour values.

        """
        sat = 100
        lum = randint(25, 50)  # prevents being too bright or too dark

        return "hsl({}, {}%, {}%)".format(hue, sat, lum)

    def colour_func_frequency(word,
                              **kwargs):
        """
        Set the luminosity of each word according to their frequency/word
        count, where the most frequent word receives the max luminosity of 50.

        Parameters
        ----------
        word : str
            The word being plotted.

        Other Parameters
        ----------------
        **kwargs
            Keyword arguments passed to the colour function of the wordcloud.

        Returns
        -------
        str
            String containing HSL colour values.

        """
        # normalise frequencies
        data_norm = (fromiter(data.values(), dtype=float)
                     - min(data.values())) \
            / (max(data.values()) - min(data.values()))

        # get index of the current word
        word_index = list(data.keys()).index(word)

        # set saturation and luminosity values
        sat = 100
        lum = 50 * data_norm[word_index]

        return "hsl({}, {}%, {}%)".format(hue, sat, lum)

    def colour_func_rank(word,
                         **kwargs):
        """
        Set the luminosity of each word according to their rank, where the
        word with rank=1 receives the max luminosity of 50.

        Parameters
        ----------
        word : str
            The word being plotted.

        Other Parameters
        ----------------
        **kwargs
            Keyword arguments passed to the colour function of the wordcloud.

        Returns
        -------
        str
            String containing HSL colour values.

        """
        # sort according to ascending values
        data_ranked = {k: v for k, v in sorted(data.items(),
                                               key=lambda item: item[1])}

        # get index of the current word
        word_index = list(data_ranked.keys()).index(word)

        # set saturation and luminosity values
        sat = 100
        lum = (50 * word_index) / len(data_ranked)

        return "hsl({}, {}%, {}%)".format(hue, sat, lum)

    # set colour function according to user input
    if colour_func == "random":
        func = colour_func_random
    elif colour_func == "frequency":
        func = colour_func_frequency
    elif colour_func == "rank":
        func = colour_func_rank

    # create wordcloud
    wc = WordCloud(mask=mask,
                   background_color=None,
                   mode="RGBA",
                   scale=rendering_quality,
                   color_func=func,
                   min_font_size=min_font_size,
                   max_font_size=max_font_size,
                   max_words=max_words,
                   relative_scaling=relative_scaling,
                   prefer_horizontal=prefer_horizontal,
                   repeat=repeat
                   )

    wc.generate_from_frequencies(data)

    img_array = wc.to_array()
    ax.imshow(img_array, extent=bbox, origin='upper',
              aspect=None, interpolation='antialiased')


def plot_contour(shaperecord, ax, bbox, resolution=100):
    """
    Plot the borders of the regions on the map.

    Parameters
    ----------
    shaperecord : shapefile.ShapeRecord
        ShapeRecord object of shapefile module containing information about a
        single NUTS region.
    ax : matplotlib.Axes class
        An instance of the matplotlib Axes class to which the wordcloud is
        plotted to.
    bbox : tuple
        Tuple containing (minX, maxX, minY, maxY) bounding box values of the
        region.
    resolution : str (default = 100)
        DPI (dots per inch) value used to generate mask image. Higher values
        create sharper regional border lines but take longer to run.

    """
    contour = get_mask(shaperecord, fill_colour=None,
                       contour_colour="black", resolution=resolution)
    ax.imshow(contour, extent=bbox, origin='upper',
              aspect=None, interpolation='antialiased')


def wordcloud_map(df,
                  nuts_codes,
                  words,
                  word_counts,
                  scale=2.0,
                  rendering_quality=1,
                  colour_func="random",
                  colour_hue=None,
                  min_font_size=4,
                  max_font_size=None,
                  max_words=200,
                  relative_scaling=0.5,
                  prefer_horizontal=0.9,
                  repeat=False,
                  border_scale="01M",
                  border_sharpness=100,
                  nuts_year=2021,
                  coord_system=3857,
                  shapefiles_path=None
                  ):
    """
    Create a wordcloud map using data from a DataFrame.

    Parameters
    ----------
    df : DataFrame
        DataFrame object containing columns with NUTS codes, words and word
        counts.
    nuts_codes : str
        Name of the column in the DataFrame containing the NUTS codes.
    words : str
        Name of the column in the DataFrame containing the words.
    word_counts : str
        Name of the column in the DataFrame containing the word counts.
    scale : float (default = 2.0)
        The scale of the produced figure. The given value works as a multiplier
        of matplotlib's default figure size. If ``scale = 1.0``, retains
        default figure size. If ``scale > 1.0``, figure gets bigger by a factor
        of scale (e.g. 1.5 means 50% bigger). If ``scale < 1.0``, figure gets
        smaller by a factor of scale (e.g. 0.5 means 50% smaller).
    rendering_quality : int (default = 1)
        The rendering quality of the words in the wordcloud. Higher values
        produce better-looking / sharper words but take longer to run.
    colour_func : str (default = "random")
        String indicating which colour function to use. Available values:
        ``"random"`` sets a random luminosity between 0 and 50 for each word
        within a region.
        ``"frequency"`` sets the luminosity of each word according to their
        relative frequency or word count, e.g. if the most frequent word A has
        value 100 and the second most frequent word B has value 50, word A
        receives a luminosity = 50 and word B = 25.
        Produces best results when ``relative_scaling = 1``.
        ``"rank"`` sets the luminosity of each word according to their absolute
        rank, e.g. if there are 5 words, the most frequent word receives
        luminosity = 50, the second most frequent receives luminosity = 40,
        and so on.
        Produces best results when ``relative_scaling = 0``.
    colour_hue : int or None (default = None)
        Sets one specific hue in the HSL colour system for all regions.
        Choose an integer between 0 and 360.
    min_font_size : int (default = 4)
        Smallest font size to use. Word placement will stop when there is no
        more room to fit words of this size.
    max_font_size : int or None (default = None)
        Maximum font size for the largest word. If None, a relative sizing
        based on the height of the image is used.
    max_words : int (default = 200)
        Maximum number of words to be included in wordcloud for each region.
    relative_scaling : float (default = 'auto')
        Importance of relative word frequencies for font-size. With
        ``relative_scaling = 0``, only the ranking of words is considered. With
        ``relative_scaling = 1``, a word that is twice as frequent will have
        twice the size. In datasets with highly uneven word frequencies,
        relative_scaling = 1 might lead to very few words being fitted, so a
        value of around 0.5 often looks better. If ``relative_scaling =
        'auto'`` it will be set to 0.5 unless ``repeat = True``, in which case
        it will be set to 0.
    prefer_horizontal : float (default = 0.9)
        The ratio of times to try horizontal fitting as opposed to vertical. If
        ``prefer_horizontal = 1``, no words will be placed vertically. If
        ``prefer_horizontal < 1``, the algorithm will try rotating the word if
        it doesn't fit.
    repeat : bool (default = False)
        Whether to repeat already-placed words until ``max_words`` or
        ``min_font_size`` is reached.
    border_scale : str (default = "01M")
        How detailed the regions' borders (i.e. the polygon shapefiles) should
        be, based on the official NUTS values used to download shapefiles.
        Smaller scales (e.g. "03M") mean more detailed polygon shapes and thus
        longer running times. Larger scales (e.g. "60M") mean less detailed
        polygon shapes and thus shorter running times. Available values:
        ``"60M"``, ``"20M"``, ``"10M"``, ``"03M"`` or ``"01M"``. For a visual
        explanation, see
        https://raw.githubusercontent.com/ropengov/giscoR/master/img/README-example-1.png
    border_sharpness : float or int (default = 100)
        Defines how sharp the regions' border lines look. Higher values create
        sharper regional border lines but might take considerably longer to
        run. Change to higher values if zooming into the map is necessary.
        The value used relates to the DPI (dots per inch) used when generating
        the mask images.
    nuts_year : int (default = 2021)
        The year of NUTS regulation, e.g. 2021, 2016, 2013, 2010, 2006 or 2003.
    coord_system : int (default = 3857)
        4-digit EPSG code (a unique identifier for different coordinate
        systems). Available values: ``4326`` (WGS84, coordinates in decimal
        degrees), ``3035`` (ETRS 1989 in Lambert Azimutal projection with
        centre in E52N10, coordinates in meters), ``3857`` (WGS84 Web Mercator
        Auxiliary Sphere, coordinates in meters).
    shapefiles_path : string or None (default = None)
        Reads shapefiles from a local filepath instead of downloading from
        GISCO's database as per default. Useful when internet access is
        limited. Works with .shp or .zip files.
        To get local files, visit:
        https://ec.europa.eu/eurostat/de/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts

    Returns
    -------
    matplotlib.figure.Figure
        The wordcloud map as a matplotlib Figure object.

    """
    if shapefiles_path != None:
        shapefiles = Reader(shapefiles_path)
    else:
        shapefiles = download_shapefiles(border_scale, nuts_year, coord_system)

    unique_codes = get_unique_codes(df, nuts_codes)
    Xmin, Ymin, Xmax, Ymax = get_bbox_map(shapefiles, unique_codes)

    fig = plt.figure()
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    ax.margins(x=0, y=0, tight=True)
    fig.add_axes(ax)
    ax.set_xlim(Xmin, Xmax)
    ax.set_ylim(Ymin, Ymax)

    for i, shaperecord in enumerate(shapefiles.shapeRecords()):
        if shaperecord.record.NUTS_ID in unique_codes:
            mask = get_mask(shaperecord, resolution=100)
            data = get_data(df,
                            nuts_codes,
                            words,
                            word_counts,
                            shaperecord.record.NUTS_ID,
                            max_words)
            bbox = get_bbox_region(shaperecord)
            plot_contour(shaperecord,
                         ax,
                         bbox,
                         resolution=border_sharpness)
            plot_region(mask=mask,
                        data=data,
                        ax=ax,
                        bbox=bbox,
                        colour_func=colour_func,
                        colour_hue=colour_hue,
                        rendering_quality=rendering_quality,
                        min_font_size=min_font_size,
                        max_font_size=max_font_size,
                        max_words=max_words,
                        relative_scaling=relative_scaling,
                        prefer_horizontal=prefer_horizontal,
                        repeat=repeat
                        )

    # get current size and multiply that by the given scale
    width, height = fig.get_size_inches()*scale
    fig.set_size_inches(width, height)
    dpi = fig.dpi
    print(
        f"Figure successfully produced with width {int(width*dpi)}px \
and height {int(height*dpi)}px.")

    return fig
