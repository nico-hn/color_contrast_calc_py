ColorContrastCalc
=================

ColorContrastCalc is a utility that helps you choose colors with
sufficient contrast, WCAG 2.0 in mind.



Installation
------------

.. code-block:: bash

    $ pip install color_contrast_calc

Usage
-----



Example 1: Calculate the contrast ratio between two colors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to calculate the contrast ratio between yellow and black,
save the following code as yellow_black_contrast.py

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

For getting grayscale, :class:`Color` has an instance method
:meth:`new_grayscale_color`.
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

And other than :meth:`new_grayscale_color`, following instance methods
are available for :class:`Color`:

* :meth:`new_brightness_color`
* :meth:`new_contrast_color`
* :meth:`new_hue_rotate_color`
* :meth:`new_invert_color`
* :meth:`new_saturate_color`
