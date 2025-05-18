#!/bin/bash

python3 encoder.py photos/baboon_ascii.pgm   bins/baboon_ascii.bin
python3 encoder.py photos/quadrado_ascii.pgm bins/quadrado_ascii.bin
python3 encoder.py photos/lena_ascii.pgm     bins/lena_ascii.bin

python3 decoder.py bins/baboon_ascii.bin   recs/baboon_ascii-rec.pgm
python3 decoder.py bins/quadrado_ascii.bin recs/quadrado_ascii-rec.pgm
python3 decoder.py bins/lena_ascii.bin     recs/lena_ascii-rec.pgm

du -b photos/baboon_ascii.pgm
du -b photos/quadrado_ascii.pgm
du -b photos/lena_ascii.pgm

du -b bins/baboon_ascii.bin
du -b bins/quadrado_ascii.bin
du -b bins/lena_ascii.bin

du -b recs/baboon_ascii-rec.pgm
du -b recs/quadrado_ascii-rec.pgm
du -b recs/lena_ascii-rec.pgm