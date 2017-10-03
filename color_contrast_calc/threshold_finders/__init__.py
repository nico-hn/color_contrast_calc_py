def binary_search_width(init_width, min):
    i = 1
    init_width = float(init_width)
    d = init_width / pow(2, i)

    while d > min:
        yield d
        i = i + 1
        d = init_width / pow(2, i)
