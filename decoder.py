#!/bin/python3

import sys
import struct
from bitstring import BitStream, BitArray
from get_string import convert_to_string_file
import os


TOTAL_BITS = 32
MAX_RANGE = 1 << TOTAL_BITS
HALF = MAX_RANGE >> 1
QUARTER = HALF >> 1
THREE_QUARTERS = QUARTER * 3


def read_compressed_file(filename):
    with open(filename, "rb") as f:
        total_bits = struct.unpack(">I", f.read(4))[0]
        count0 = struct.unpack(">I", f.read(4))[0]
        count1 = struct.unpack(">I", f.read(4))[0]
        data = f.read()
        bitstream = BitStream(bytes=data)
    return total_bits, count0, count1, bitstream


def arithmetic_decode_with_scaling(bitstream, count0, count1, total_symbols):
    total = count0 + count1
    prob0 = count0 / total

    low = 0
    high = MAX_RANGE
    value = 0

    for _ in range(TOTAL_BITS):
        value = (value << 1) | bitstream.read("uint:1")

    decoded_bits = []

    for _ in range(total_symbols):
        range_ = high - low
        threshold = ((value - low + 1) * total - 1) // range_

        if threshold < count0:
            bit = 0
            high = low + int(range_ * prob0)
        else:
            bit = 1
            low = low + int(range_ * prob0)

        decoded_bits.append(bit)

        while True:
            if high <= HALF:
                pass
            elif low >= HALF:
                low -= HALF
                high -= HALF
                value -= HALF
            elif QUARTER <= low and high <= THREE_QUARTERS:
                low -= QUARTER
                high -= QUARTER
                value -= QUARTER
            else:
                break

            low <<= 1
            high <<= 1
            value = (value << 1) | (
                bitstream.read("uint:1") if bitstream.pos < bitstream.len else 0
            )
            high = min(high, MAX_RANGE)

    return decoded_bits


def write_binary_file(bits, output_filename):
    bit_array = BitArray(bits)
    with open(output_filename, "wb") as f:
        bit_array.tofile(f)


def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    _, count0, count1, bitstream = read_compressed_file(input_file)
    total_symbols = count0 + count1
    bits = arithmetic_decode_with_scaling(bitstream, count0, count1, total_symbols)
    tmp_output_file = "tmpfile"
    write_binary_file(bits, tmp_output_file)
    convert_to_string_file(tmp_output_file,output_file)
    os.remove(tmp_output_file)


if __name__ == "__main__":
    main()
