Features and usage
===================

1. To start using *wordcloud_mapper*, import the package with::

    import wordcloud_mapper as wcm


2. Then use any of the following functions to generate and customize you wordcloud_map:

.. toctree::
   :maxdepth: 4

   functions

3. When you're happy with the results, save the image to the desired format (png, jpeg, svg, etc.) using::

    map = wcm.wordcloud_map() # the generated matplotlib figure
    map.savefig("path_to_image.png") # choose image format