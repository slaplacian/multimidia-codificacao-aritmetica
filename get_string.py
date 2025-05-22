def convert_to_string_file(input_path, output_path):

    with open(input_path, 'rb') as f:
        magic_number = f.readline().strip()
        if magic_number != b'BYTES':
            raise ValueError('Formato inválido.')

        while True:
            line = f.readline()
            if not line.startswith(b'#'):
                width, height = map(int, line.strip().split())
                break

        max_val = int(f.readline().strip())

        pixel_data = list(f.read(width * height))

    with open(output_path, 'w') as f:
        f.write('P2\n')
        f.write(f'{width} {height}\n')
        f.write(f'{max_val}\n')
        for i in range(0, len(pixel_data), width):
            linha = ' '.join(str(p) for p in pixel_data[i:i+width])
            f.write(f'{linha}\n')
