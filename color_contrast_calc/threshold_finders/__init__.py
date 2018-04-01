'''Collection of modules that implement the main logic of instance
methods of Color, ``.find_*_threshold``.
'''

def binary_search_width(init_width, min_width):
    i = 1
    init_width = float(init_width)
    d = init_width / pow(2, i)

    while d > min_width:
        yield d
        i += 1
        d = init_width / pow(2, i)


def rgb_with_better_ratio(other_rgb, criteria, r, sufficient_r, calc_rgb):
    nearest = calc_rgb(other_rgb, r)
    satisfying_nearest = criteria.has_sufficient_contrast(nearest)

    if sufficient_r and not satisfying_nearest:
        return calc_rgb(other_rgb, sufficient_r)

    return nearest
