==================
AFDesign Extractor
==================
NOTE: This project is a work-in-progress.

Currently the extracting resources from a afdesign is working. but parsing the data further than that hasn't been accomplished yet.

Purpose
=======
It'd be useful to have a command line tool / library that will extract resources from a afdesign and convert each slice to a SVG/PNG/JPG/Whatever. 

Also: I like mucking around in file-formats.

Extracting the test data
========================
You can extract the test data using this shell one liner, or do them one at a time by using ``main.py``:

.. code-block:: sh

    $ for f in testDesigns/*; do ./main.py "$f" data/$(basename "$f" .afdesign); done

Documentation
=============

I have what I have documented current available at the `GitHub Pages <http://nickbeeuwsaert.github.io/AFDesignLoad>`_ site

API structyre us currently under construction. I'd like something like this

.. code-block:: sh

    from afdesinload import AFD

    afd = AFD("file.afdesign")

    afd.docs # -> Binary blobs
    afd.layers # -> List of afdesign.Layer
    afd.shapes # -> List of afdesign.Shape
    afd.size # -> tuple of (width, height)
