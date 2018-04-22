import color_contrast_calc as calc

yellow = calc.color_from('yellow')
orange = calc.color_from('orange')


report = 'The grayscale of {:s} ({:s}) is {:s}'

print(report.format(yellow.hex, yellow.name,
                    yellow.with_grayscale().hex))
print(report.format(orange.hex, orange.name,
                    orange.with_grayscale().hex))
