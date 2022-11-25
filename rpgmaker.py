#!/usr/bin/env python3
import lzstring
import json


def decode(save):
    lz = lzstring.LZString()
    decoded = lz.decompressFromBase64(save)
    parsed = json.loads(decoded)
    decoded = json.dumps(parsed, indent=4, sort_keys=True)
    return decoded


def encode(save):
    lz = lzstring.LZString()
    encoded = lz.compressToBase64(save)
    return encoded
