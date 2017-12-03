import color_contrast_calc as calc

yellow = calc.color_from('yellow')
black = calc.color_from('black')

contrast_ratio = yellow.contrast_ratio_against(black)

report = 'The contrast ratio between {:s} and {:s} is {:f}'
print(report.format(yellow.name, black.name, contrast_ratio))
print(report.format(yellow.hex, black.hex, contrast_ratio))
