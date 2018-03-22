import math

from .. import checker


class SearchDirection:
    def __init__(self, level, fixed_rgb):
        self.level = level
        self.target_ratio = checker.level_to_ratio(level)
        self.fixed_luminance = checker.relative_luminance(fixed_rgb)

    def has_sufficient_contrast(self, rgb):
        return self.contrast_ratio(rgb) >= self.target_ratio

    def contrast_ratio(self, rgb):
        luminance = checker.relative_luminance(rgb)
        return checker.luminance_to_contrast_ratio(self.fixed_luminance,
                                                   luminance)


class ToDarkerSide(SearchDirection):
    def round(self, r):
        return math.floor(r * 10) / 10.0

    def increment_condition(self, contrast_ratio):
        return contrast_ratio > self.target_ratio


class ToBrighterSide(SearchDirection):
    def round(self, r):
        return math.ceil(r * 10) / 10.0

    def increment_condition(self, contrast_ratio):
        return self.target_ratio > contrast_ratio


def threshold_criteria(level, fixed_color, other_color):
    if should_scan_darker_side(fixed_color, other_color):
        return ToDarkerSide(level, fixed_color.rgb)

    return ToBrighterSide(level, fixed_color.rgb)


def should_scan_darker_side(fixed_color, other_color):
    fixed_luminance = checker.relative_luminance(fixed_color.rgb)
    other_luminance = checker.relative_luminance(other_color.rgb)
    higher_luminance = fixed_luminance > other_luminance
    same_luminance = fixed_luminance == other_luminance
    is_light_color = checker.is_light_color(fixed_color.rgb)

    return higher_luminance or (is_light_color and same_luminance)
