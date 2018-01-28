import color_contrast_calc as calc
from color_contrast_calc.color import Color

# Create an instance of Color from a hex code
# (You can pass 'red' or (255, 0, 0) instead of '#ff0000')
red = calc.color_from('#ff0000')

print(isinstance(red, Color))
print(red.name)
print(red.hex)
print(red.rgb)
print(red.hsl)
