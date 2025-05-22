#!/bin/python3

import sys
import struct
from bitstring import ConstBitStream, BitArray
from get_bytes import convert_to_bytes_file
import os


TOTAL_BITS = 32
MAX_RANGE = (1 << TOTAL_BITS)
HALF = MAX_RANGE >> 1
QUARTER = HALF >> 1
THREE_QUARTERS = QUARTER * 3

def get_bit_list(filename):
    p5_filename = "tmpfile"
    convert_to_bytes_file(filename,p5_filename)
    stream = ConstBitStream(filename=p5_filename)
    os.remove(p5_filename)
    return [int(b) for b in stream]

def calculate_frequencies(bits):
    count = [0, 0]
    for bit in bits:
        count[bit] += 1
    total = sum(count)
    return count, [c / total for c in count]

def arithmetic_encode_with_scaling(bits, freq):
    low = 0
    high = MAX_RANGE
    pending_bits = 0
    output_bits = []

    for bit in bits:
        range_ = high - low
        if bit == 0:
            high = low + int(range_ * freq[0])
        else:
            low = low + int(range_ * freq[0])

        while True:
            if high <= HALF:
                output_bits.append(0)
                output_bits.extend([1] * pending_bits)
                pending_bits = 0
                low <<= 1
                high <<= 1
            elif low >= HALF:
                output_bits.append(1)
                output_bits.extend([0] * pending_bits)
                pending_bits = 0
                low = (low - HALF) << 1
                high = (high - HALF) << 1
            elif QUARTER <= low and high <= THREE_QUARTERS:
                pending_bits += 1
                low = (low - QUARTER) << 1
                high = (high - QUARTER) << 1
            else:
                break
            high = min(high, MAX_RANGE)

    pending_bits += 1
    if low < QUARTER:
        output_bits.append(0)
        output_bits.extend([1] * pending_bits)
    else:
        output_bits.append(1)
        output_bits.extend([0] * pending_bits)

    return output_bits

def write_binary_file(output_filename, total_bits, count0, count1, output_bits):
    with open(output_filename, 'wb') as f:
        
        f.write(struct.pack('>I', total_bits))
        f.write(struct.pack('>I', count0))
        f.write(struct.pack('>I', count1))

        bit_array = BitArray(output_bits)
        bit_array.tofile(f)

def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    bits = get_bit_list(input_file)
    count, freq = calculate_frequencies(bits)
    output_bits = arithmetic_encode_with_scaling(bits, freq)

    write_binary_file(output_file, len(output_bits), count[0], count[1], output_bits)

if __name__ == '__main__':
    main()