from color_contrast_calc.color import Color

yellow = Color.from_name('yellow')
orange = Color.from_name('orange')

report = 'The contrast ratio between {:s} and {:s} is {:f}'

# Find brightness adjusted colors.

a_orange = yellow.find_brightness_threshold(orange, 'A')
a_contrast_ratio = yellow.contrast_ratio_against(a_orange)

aa_orange = yellow.find_brightness_threshold(orange, 'AA')
aa_contrast_ratio = yellow.contrast_ratio_against(aa_orange)

print('# Brightness adjusted colors')
print(report.format(yellow.hex, a_orange.hex, a_contrast_ratio))
print(report.format(yellow.hex, aa_orange.hex, aa_contrast_ratio))


# Find lightness adjusted colors.

a_orange = yellow.find_lightness_threshold(orange, 'A')
a_contrast_ratio = yellow.contrast_ratio_against(a_orange)

aa_orange = yellow.find_lightness_threshold(orange, 'AA')
aa_contrast_ratio = yellow.contrast_ratio_against(aa_orange)

print('# Lightness adjusted colors')
print(report.format(yellow.hex, a_orange.hex, a_contrast_ratio))
print(report.format(yellow.hex, aa_orange.hex, aa_contrast_ratio))
