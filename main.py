import re as re

import regex as rx

# base: \w+[+*?]?[+?]?
# \w+[+*?]?[+?]?
# (\w+[+*?]?[+?]?)*((\((\w+[+*?]?[+?]?|(?R))+\))+[+*?]?[+?]?)*

# vesrion with parentesis
# all = (\w+[+*?]?[+?]?)*((\((\w+[+*?]?[+?]?|(?R))+\))+[+*?]?[+?]?)+?(\w+[+*?]?[+?]?)*

m = rx.compile(r"(\w+|(\((?R)+\)))[+*?]?[+?]?(\|?(?R))?+").fullmatch("*ab")

print(m)

# \w+(\+|\*|\?)?[+?]?
# ((\w+[+*?]?[+?]?)|((\((\w+[+*?]?[+?]?|(?R))+\))+[+*?]?[+?]?))+?
# ((\w+[+*?]?[+?]?(\|?(?R))?)|((\((?R)+\))+[+*?]?[+?]?)(\|?(?R))?)+


