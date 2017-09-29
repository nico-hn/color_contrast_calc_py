# Utility functions that provide basic operations on colors given as color codes

def hex_to_rgb(hex_code):
    hex_part = __remove_head_sharp(hex_code)

    if len(hex_part) == 3:
        return list(map(lambda c: int(c, 16) * 17, hex_part))
    elif len(hex_part) == 6:
        primaries = map(lambda i: hex_part[i:(i+2)], (0, 2, 4))
        return list(map(lambda c: int(c, 16), primaries))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def __remove_head_sharp(hex_code):
    if hex_code.find('#') == 0:
        return hex_code[1:]

    return hex_code
