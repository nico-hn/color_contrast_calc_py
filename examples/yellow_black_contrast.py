from color_contrast_calc.color import Color

yellow = Color.from_name('yellow')
black = Color.from_name('black')

contrast_ratio = yellow.contrast_ratio_against(black)

report = 'The contrast ratio between {:s} and {:s} is {:f}'
print(report.format(yellow.name, black.name, contrast_ratio))
print(report.format(yellow.hex, black.hex, contrast_ratio))
