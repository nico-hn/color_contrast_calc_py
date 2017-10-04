def binary_search_width(init_width, min_width):
    i = 1
    init_width = float(init_width)
    d = init_width / pow(2, i)

    while d > min_width:
        yield d
        i += 1
        d = init_width / pow(2, i)
