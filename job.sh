#!/bin/bash

python3 encoder.py photos/baboon_ascii.pgm   bins/baboon_ascii.bin
python3 encoder.py photos/quadrado_ascii.pgm bins/quadrado_ascii.bin
python3 encoder.py photos/lena_ascii.pgm     bins/lena_ascii.bin

python3 decoder.py bins/baboon_ascii.bin   recs/baboon_ascii-rec.pgm
python3 decoder.py bins/quadrado_ascii.bin recs/quadrado_ascii-rec.pgm
python3 decoder.py bins/lena_ascii.bin     recs/lena_ascii-rec.pgm

get_size() {
  if [[ "$OSTYPE" == "darwin"* ]]; then
    stat -f%z "$1"
  else
    du -b "$1" | cut -f1
  fi
}

echo "Original images:"
for f in photos/*.pgm; do
  echo -n "$f: "
  get_size "$f"
done

echo -e "\nEncoded binaries:"
for f in bins/*.bin; do
  echo -n "$f: "
  get_size "$f"
done

echo -e "\nReconstructed images:"
for f in recs/*.pgm; do
  echo -n "$f: "
  get_size "$f"
done
