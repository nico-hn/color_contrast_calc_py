import color_contrast_calc as calc
import color_contrast_calc.sorter as sorter

color_names = ['red', 'yellow', 'lime', 'cyan', 'fuchsia', 'blue']
colors = [calc.color_from(c) for c in color_names]

# Sort by hSL order.  An uppercase for a component of color means
# that component should be sorted in descending order.

hsl_ordered = sorter.sorted(colors, "hSL")
print ("Colors sorted in the order of hSL:")
print([c.name for c in hsl_ordered])

# Sort by RGB order.

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
