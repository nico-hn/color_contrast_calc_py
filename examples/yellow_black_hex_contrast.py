from color_contrast_calc import checker

yellow = '#ff0'
black = '#000000'
# or
# yellow = (255, 255, 0)
# black = (0, 0, 0)

ratio = checker.contrast_ratio(yellow, black)
level = checker.ratio_to_level(ratio)

report = 'The contrast ratio between yellow and black: {:f}'

print(report.format(ratio))
print('Level: {:s}'.format(level))
