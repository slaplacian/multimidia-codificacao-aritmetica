def convert_to_bytes_file(input_path, output_path):
    with open(input_path, 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines if line.strip() and not line.startswith('#')]

    if lines[0] != 'P2':
        raise ValueError('Formato inválido. Esperado P2.')

    width, height = map(int, lines[1].split())
    max_val = int(lines[2])

    pixel_values = []
    for line in lines[3:]:
        pixel_values.extend(map(int, line.split()))

    if len(pixel_values) != width * height:
        raise ValueError('Quantidade de pixels não corresponde à dimensão informada.')

    with open(output_path, 'wb') as f:
        f.write(b'BYTES\n')
        f.write(f'{width} {height}\n'.encode())
        f.write(f'{max_val}\n'.encode())
        f.write(bytearray(pixel_values))
