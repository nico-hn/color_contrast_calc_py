import color_contrast_calc.color

# Named colors
named_colors = color_contrast_calc.color.NAMED_COLORS

print('The number of named colors: ', end='')
print(len(named_colors))
print('The first color of named colors: ', end='')
print(named_colors[0].name)
print('The last color of named colors: ', end='')
print(named_colors[-1].name)

# Web safe colors
web_safe_colors = color_contrast_calc.color.WEB_SAFE_COLORS

print('The number of web safe colors: ', end='')
print(len(web_safe_colors))
print('The first color of web safe colors: ', end='')
print(web_safe_colors[0].name)
print('The last color of web safe colors: ', end='')
print(web_safe_colors[-1].name)

# HSL colors
hsl_colors = color_contrast_calc.color.hsl_colors()

print('The number of HSL colors: ', end='')
print(len(hsl_colors))
print('The first color of HSL colors: ', end='')
print(hsl_colors[0].name)
print('The 60th color of HSL colors: ', end='')
print(hsl_colors[60].name)
print('The 120th color of HSL colors: ', end='')
print(hsl_colors[120].name)
print('The last color of HSL colors: ', end='')
print(hsl_colors[-1].name)
