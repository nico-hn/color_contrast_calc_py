ColorContrastCalc
=================

ColorContrastCalc is a utility that helps you choose colors with
sufficient contrast, WCAG 2.0 in mind.



Installation
------------

(Not published yet on PyPI)

.. code-block:: bash

    $ pip install color_contrast_calc

Usage
-----



Example 1: Calculate the contrast ratio between two colors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to calculate the contrast ratio between yellow and black,
save the following code as yellow_black_contrast.py:

.. code-block:: python

    from color_contrast_calc.color import Color

    yellow = Color.from_name('yellow')
    black = Color.from_name('black')

    contrast_ratio = yellow.contrast_ratio_against(black)

    report = 'The contrast ratio between {:s} and {:s} is {:f}'

    print(report.format(yellow.name, black.name, contrast_ratio))
    print(report.format(yellow.hex, black.hex, contrast_ratio))

Then execute the script:

.. code-block:: bash

    $ python yellow_black_contrast.py
    The contrast ratio between yellow and black is 19.556000
    The contrast ratio between #ffff00 and #000000 is 19.556000


Example 2: Find colors that have enough contrast ratio with a given color
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to find a combination of colors with sufficient contrast
by changing the brightness/lightness of one of those colors, save the
following code as yellow_orange_contrast.py:

.. code-block:: python

    from color_contrast_calc.color import Color

    yellow = Color.from_name('yellow')
    orange = Color.from_name('orange')


    # Find brightness adjusted colors.

    a_orange = yellow.find_brightness_threshold(orange, 'A')
    a_contrast_ratio = yellow.contrast_ratio_against(a_orange)

    aa_orange = yellow.find_brightness_threshold(orange, 'AA')
    aa_contrast_ratio = yellow.contrast_ratio_against(aa_orange)

    report = 'The contrast ratio between {:s} and {:s} is {:f}'

    print('# Brightness adjusted colors')
    print(report.format(yellow.hex, a_orange.hex, a_contrast_ratio))
    print(report.format(yellow.hex, aa_orange.hex, aa_contrast_ratio))


    # Find lightness adjusted colors.

    a_orange = yellow.find_lightness_threshold(orange, 'A')
    a_contrast_ratio = yellow.contrast_ratio_against(a_orange)

    aa_orange = yellow.find_lightness_threshold(orange, 'AA')
    aa_contrast_ratio = yellow.contrast_ratio_against(aa_orange)

    report = 'The contrast ratio between {:s} and {:s} is {:f}'

    print('# Lightness adjusted colors')
    print(report.format(yellow.hex, a_orange.hex, a_contrast_ratio))
    print(report.format(yellow.hex, aa_orange.hex, aa_contrast_ratio))

Then execute the script:

.. code-block:: bash

    $ python yellow_orange_contrast.py
    # Brightness adjusted colors
    The contrast ratio between #ffff00 and #c68000 is 3.013798
    The contrast ratio between #ffff00 and #9d6600 is 4.512054
    # Lightness adjusted colors
    The contrast ratio between #ffff00 and #c78000 is 3.001186
    The contrast ratio between #ffff00 and #9d6600 is 4.512054

Example 3: Grayscale of given colors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For getting grayscale, ``Color`` has an instance method
``new_grayscale_color``.
For example, save the following code as grayscale.py

.. code-block:: python

    from color_contrast_calc.color import Color

    yellow = Color.from_name('yellow')
    orange = Color.from_name('orange')

    report = 'The grayscale of {:s} ({:s}) is {:s}'

    print(report.format(yellow.hex, yellow.name,
                        yellow.new_grayscale_color().hex))
    print(report.format(orange.hex, orange.name,
                        orange.new_grayscale_color().hex))

Then execute the script:

.. code-block:: bash

    $ python grayscale.py
    The grayscale of #ffff00 (yellow) is #ededed
    The grayscale of #ffa500 (orange) is #acacac

And other than ``new_grayscale_color``, following instance methods
are available for ``Color``:

* ``new_brightness_color``
* ``new_contrast_color``
* ``new_hue_rotate_color``
* ``new_invert_color``
* ``new_saturate_color``

Example 4: Sort colors
^^^^^^^^^^^^^^^^^^^^^^

You can sort colors using a function
``color_contrast_calc.sorter.sorted``.

For example, save the following code as sort_colors.py:

.. code-block:: python

    from color_contrast_calc.color import Color
    import color_contrast_calc.sorter as sorter

    color_names = ('red', 'yellow', 'lime', 'cyan', 'fuchsia', 'blue')
    colors = [Color.from_name(c) for c in color_names]

    # sort by hSL order.  An uppercase for a component of color means
    # that component should be sorted in descending order.

    hsl_ordered = sorter.sorted(colors, "hSL")
    print ("Colors sorted in the order of hSL:")
    print([c.name for c in hsl_ordered])

    # sort by RGB order.

    rgb_ordered = sorter.sorted(colors, "RGB")
    print ("Colors sorted in the order of RGB:")
    print([c.name for c in rgb_ordered])

    # You can also change the precedence of components.

    grb_ordered = sorter.sorted(colors, "GRB")
    print ("Colors sorted in the order of GRB:")
    print([c.name for c in grb_ordered])

    # And you can directly sort hex color codes.

    ## Hex color codes that correspond to the color_names given above.
    hex_codes = ['#ff0000', '#ff0', '#00ff00', '#0ff', '#f0f', '#0000FF']

    hsl_ordered = sorter.sorted(hex_codes, "hSL")
    print("Hex codes sorted in the order of hSL:")
    print(hsl_ordered)

Then execute the script:

.. code-block:: bash

    $ python sort_colors.py
    Colors sorted in the order of hSL:
    ['red', 'yellow', 'lime', 'cyan', 'blue', 'fuchsia']
    Colors sorted in the order of RGB:
    ['yellow', 'fuchsia', 'red', 'cyan', 'lime', 'blue']
    Colors sorted in the order of GRB:
    ['yellow', 'cyan', 'lime', 'fuchsia', 'red', 'blue']
    Hex codes sorted in the order of hSL:
    ['#ff0000', '#ff0', '#00ff00', '#0ff', '#0000FF', '#f0f']
