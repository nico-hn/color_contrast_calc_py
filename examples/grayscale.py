from color_contrast_calc.color import Color

yellow = Color.from_name('yellow')
orange = Color.from_name('orange')


report = 'The grayscale of {:s} ({:s}) is {:s}'

print(report.format(yellow.hex, yellow.name,
                    yellow.new_grayscale_color().hex))
print(report.format(orange.hex, orange.name,
                    orange.new_grayscale_color().hex))
