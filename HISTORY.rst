=======
History
=======

0.1.0 (2022-07-27)
------------------

* First release on PyPI.


0.2.0 (not published on PyPI yet)
---------------------------------

New functionality:
* Add new function ``calc_tfidf()`` to calculate TF-IDF score of each word in each region in a dataframe.
* Add wordcloud colour generating function based on rank of words.
* Add colour_hue parameter to wordcloud_map() allowing users to choose one specific colour hue for all regions.


Parameters exposed to users:
* Allow users to change the parameters when downloading NUTS shapefiles from Eurostat's API in wordcloud_map().
* Allow users to change the sharpness of the regional border lines by channging the DPI value used when creating the masks.
* Allow users to use shapefiles form a local filepath instead of downloading from GISCO's online database.

Others:
* Change default coordination system when downloading shapefiles.
