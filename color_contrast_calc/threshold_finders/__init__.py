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


def find_ratio(other_rgb, criteria, rgb_with_ratio, init_ratio, init_width):
    target_contrast = criteria.target_contrast
    r = init_ratio
    passing_r = None

    for d in binary_search_width(init_width, 0.01):
        new_ratio = criteria.contrast_ratio(rgb_with_ratio(other_rgb, r))

        if new_ratio >= target_contrast:
            passing_r = r

        if new_ratio == target_contrast:
            break

        r += d if criteria.increment_condition(new_ratio) else -d

    return (r, passing_r)


def rgb_with_better_ratio(color, criteria, last_r, passing_r, rgb_with_ratio):
    closest = rgb_with_ratio(color, last_r)

    if passing_r and not criteria.has_sufficient_contrast(closest):
        return rgb_with_ratio(color, passing_r)

    return closest
