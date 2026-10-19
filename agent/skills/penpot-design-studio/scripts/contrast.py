#!/usr/bin/env python3
"""Contrast for solid opaque sRGB hex colors; not a rendered UI certification."""
import argparse
import json
import re


def color(value):
    value = value.lstrip("#")
    if re.fullmatch(r"[0-9a-fA-F]{3}", value):
        value = "".join(c * 2 for c in value)
    if not re.fullmatch(r"[0-9a-fA-F]{6}", value):
        raise argparse.ArgumentTypeError("Use an opaque #RGB or #RRGGBB color")
    return value.upper()


def luminance(value):
    channels = [int(value[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return sum(c * w for c, w in zip(linear, (0.2126, 0.7152, 0.0722)))


def contrast(foreground, background):
    a, b = sorted((luminance(foreground), luminance(background)))
    return (b + 0.05) / (a + 0.05)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("foreground", type=color)
    parser.add_argument("background", type=color)
    args = parser.parse_args()
    ratio = contrast(args.foreground, args.background)
    print(json.dumps({"ratio": round(ratio, 3), "normal_text_AA": ratio >= 4.5,
                      "large_text_AA": ratio >= 3, "normal_text_AAA": ratio >= 7,
                      "scope": "opaque sRGB pair only; verify actual rendered surface"}, indent=2))
