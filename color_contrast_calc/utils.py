# Utiity functions that provide basic operations on colors given as color codes

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)
