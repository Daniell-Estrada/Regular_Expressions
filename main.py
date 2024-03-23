import re as re

import regex as rx

m = rx.compile(r"([\w\d]+[\+\*\?]*)*((\(([^()]|(?R))+\))+[\+\*\?]*)*").fullmatch(
    "ab*(a+b(dc)*)*", re.VERBOSE)

print(m)

