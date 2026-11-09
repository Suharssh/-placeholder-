"""
This file normalizes and removes the spl characters in artist's name, and makes it uniform for further 
preprocessing 

"""


from __future__ import annotations
import re
import unicodedata
regex = re.compile(r"[^\w\s]")
def normalize(text: str) -> str:
   #convert to lowercase
    folded = text.casefold()

    #removes the dilemna of accented chars, like beyonce's -> separates the accented chars
    decomposed = unicodedata.normalize("NFKD", folded)

    # throw away the accent marks (combining characters): "beyonce´" -> "beyonce".
    no_accents = "".join(ch for ch in decomposed if not unicodedata.combining(ch))

    # remove dots entirely
    no_dots = no_accents.replace(".", "")

    # replace any other punctuation with a space
    spaced = regex.sub(" ", no_dots)

    # prolonged and trailing spaces to be removed
    return " ".join(spaced.split())


def tokenize(text: str) -> list[str]:
    # Input is already normalized, so splitting on spaces is enough: "money trees" -> ["money", "trees"].
    return text.split()
