def bin_to_int(x):
    # Converts a string of bits to an integer.
    if not x:
        return 0
    return int(x, 2)


def hex_to_bin(x):
    # Converts a string of hexadecimal numbers to a string of bits (preserving leading zeros).
    return bin(int(x, 16))[2:].zfill(len(x) * 4)
