import random
# colors = [ 
# "LightPink", "LightSalmon", "LightSeaGreen", "LightSkyBlue", "LightSlateGray", "LightSlateGrey", "LightSteelBlue", "LightYellow", "Lime", "LimeGreen", "Linen", "Magenta", "MediumAquaMarine", "MediumBlue", "MediumOrchid", "MediumPurple", "MediumSeaGreen", "MediumSlateBlue", "MediumSpringGreen", "MediumTurquoise", "MediumVioletRed", "MidnightBlue", "MintCream", "MistyRose", "Moccasin", "OldLace", "Olive", "OliveDrab", "Orange", "OrangeRed", "Orchid", "PaleGoldenRod", "PaleGreen", "PaleTurquoise", "PaleVioletRed", "PapayaWhip", "PeachPuff", "Peru", "Pink", "Plum", "PowderBlue", "RosyBrown", "RoyalBlue", "SaddleBrown", "Salmon"]

colors = [
    "LightSeaGreen", "LightSlateGray", "LightSlateGrey",
    "Lime", "LimeGreen", "Magenta",
    "MediumAquaMarine", "MediumBlue", "MediumOrchid",
    "MediumPurple", "MediumSeaGreen", "MediumSlateBlue",
    "MediumSpringGreen", "MediumTurquoise", "MediumVioletRed",
    "MidnightBlue", "Olive", "OliveDrab",
    "Orange", "OrangeRed", "Orchid",
    "Peru", "Pink", "Plum",
    "RosyBrown", "RoyalBlue", "SaddleBrown", "Salmon",

    # Additional distinct colors
    "Red",
    "Crimson",
    "FireBrick",
    "DarkRed",
    "Blue",
    "DarkBlue",
    "Navy",
    "DodgerBlue",
    "DeepSkyBlue",
    "Teal",
    "DarkCyan",
    "ForestGreen",
    "Green",
    "DarkGreen",
    "SeaGreen",
    "SpringGreen",
    "YellowGreen",
    "Chartreuse",
    "Gold",
    "GoldenRod",
    "DarkGoldenRod",
    "Chocolate",
    "Brown",
    "Maroon",
    "Purple",
    "DarkMagenta",
    "DarkViolet",
    "BlueViolet",
    "RebeccaPurple",
    "DeepPink",
    "HotPink",
    "IndianRed",
    "Tomato",
    "Coral",
    "Turquoise",
    "SteelBlue",
    "SlateBlue"
]

def choose():
    return random.choice(colors)