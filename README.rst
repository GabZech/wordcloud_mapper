================
wordcloud_mapper
================


.. image:: https://img.shields.io/pypi/v/wordcloud_mapper.svg
        :alt: PyPI - Version
        :target: https://pypi.python.org/pypi/wordcloud_mapper

.. image:: https://img.shields.io/github/pipenv/locked/python-version/GabZech/wordcloud_mapper
        :alt: GitHub Pipenv locked Python version

.. image:: https://img.shields.io/pypi/l/wordcloud_mapper
        :alt: PyPI - License
        :target: https://github.com/GabZech/wordcloud_mapper/blob/main/LICENSE

.. image:: https://img.shields.io/github/repo-size/GabZech/wordcloud_mapper?color=white
        :alt: GitHub repo size

`wordcloud_mapper` is a Python package that allows one to **create wordclouds shaped like regions on a map**.

Such visualisations are especially useful when communicating sets of data that consist of many different observations and each observation is attributed to a specific region and size of occurrence. Take the example below, a dataset containing the name of the biggest companies (in terms of estimated number of employees in 2019) for each state in Germany.

|

.. image:: https://github.com/GabZech/wordcloud_mapper/raw/main/docs/figures/germany_nuts1.png

Installation
------------

To install `wordcloud_mapper`, run in your terminal:

.. code-block:: console

    pip install wordcloud_mapper

or

.. code-block:: console

    pip install wordcloud-mapper


Features and usage
------------------

* **Create a wordcloud map** from data stored in a DataFrame object using `wordcloud_map() <https://gabzech.github.io/wordcloud_mapper/build/html/functions.html#>`_.
* **Easily resize a map** by any desired scaling factor using `resize_map() <https://gabzech.github.io/wordcloud_mapper/build/html/functions.html#resize-map>`_.
* **Load dummy datasets** to test out the package's features using `load_companies() <https://gabzech.github.io/wordcloud_mapper/build/html/functions.html#load-companies>`_.

See the `documentation <https://GabZech.github.io/wordcloud_mapper>`_ for more information on how to use the package and its functions.


Notes on geographical nomenclature
----------------------------------

The classification of regions used here follows the European Union's Nomenclature of Territorial Units for Statistics (`NUTS <https://en.wikipedia.org/wiki/Nomenclature_of_Territorial_Units_for_Statistics>`_), a geocode standard for referencing the subdivisions of countries. The advantage of using this system is that the classification of regions across countries is **standardised and hierarchically structured**. For instance, Germany has the base code *DE* (NUTS 0), the state of Bavaria has the code *DE2* (NUTS 1), its subregion of Oberbayern has the code *DE21* (NUTS 2) and the city of Munich has the code *DE212* (NUTS 3). Since each region is given a unique identifier which is directly linked to the regional level above it, it is fairly easy to identify and match any dataset to these regions.

However, this means that **this package currently only works for creating wordcloud maps for EU countries**. For an overview of the NUTS regions and levels, you can browse the available `maps for each EU country <https://ec.europa.eu/eurostat/web/nuts/nuts-maps>`_ or use `this interactive map <https://ec.europa.eu/statistical-atlas/viewer/?config=typologies.json&>`_ instead. If you have a dataset containing postcodes and want to convert these to NUTS regions, you can find the `correspondence tables here <https://ec.europa.eu/eurostat/web/nuts/correspondence-tables/postcodes-and-nuts>`_.

In a future release, support nor non-NUTS regional referencing systems will be implemented.

Feedback and contributions
--------------------------

This package is under active development, so any feedback, recommendations, suggestions or contribution requests are more than welcome!

Please read the contribution instructions or email g.dev@posteo.net if you would like to provide any feedback.
