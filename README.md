# Codificador Aritmético

Este trabalho implementa um codificador e decodificador aritmético binário com suporte a *rescaling* para evitar underflow. A codificação aritmética é um método de compressão de dados que representa uma sequência de símbolos como um único número real entre 0 e 1, permitindo uma compressão mais eficiente que métodos tradicionais como Huffman.

## Fundamentos Técnicos

### Codificação Aritmética
- Utiliza um intervalo numérico [0,1) para representar a sequência de símbolos
- Cada símbolo subdivide o intervalo atual proporcionalmente à sua probabilidade
- Implementa *rescaling* para evitar problemas de precisão numérica
- Utiliza 32 bits de precisão para os cálculos internos
- Suporta compressão binária (símbolos 0 e 1)

### Rescaling
O algoritmo implementa três tipos de rescaling:
1. **E1**: Quando o intervalo está na primeira metade [0, 0.5)
2. **E2**: Quando o intervalo está na segunda metade [0.5, 1)
3. **E3**: Quando o intervalo está no meio [0.25, 0.75)

### Otizmização

Nesse trabalho, visando uma compressão melhor, foi analizado o padrão comum dos arquivos .PGM P2, que possuem vários valores de 0 até 255 em ASCII. esses valores foram transformados em bytes, então, espaços não são mais necessários, e cada pixel é representado por 1 byte. Antes de começar a compressão, os dados da imagem são tranformados nesse formato e só depois são comprimidos com o codificador aritmético binário.

## Uso da CLI

### Codificar uma Imagem
```bash
python encoder.py <arquivo_entrada.pgm> <arquivo_saida.bin>
```

Parâmetros:
- `arquivo_entrada.pgm`: Imagem PGM em formato ASCII para compressão
- `arquivo_saida.bin`: Arquivo binário de saída contendo o bitstream comprimido

O codificador:
1. Lê a imagem PGM de entrada
2. Calcula as frequências dos símbolos (0 e 1)
3. Aplica a codificação aritmética com rescaling
4. Salva o bitstream comprimido junto com os metadados necessários para decodificação

### Decodificar uma Imagem
```bash
python decoder.py <arquivo_entrada.bin> <arquivo_saida.pgm>
```

Parâmetros:
- `arquivo_entrada.bin`: Arquivo binário contendo o bitstream comprimido
- `arquivo_saida.pgm`: Imagem PGM de saída reconstruída

O decodificador:
1. Lê os metadados e o bitstream comprimido
2. Reconstrui a sequência original usando decodificação aritmética
3. Gera a imagem PGM reconstruída

## Análise de Compressão

### Imagem: Baboon (baboon_ascii.pgm)
- **Tamanho Original**: 1,258,676 bytes (1.2MB)
- **Tamanho Comprimido**: 262,126 bytes (256MB)
- **Taxa de Compressão**: 4.802
- **Análise**: A imagem do babuíno apresenta uma taxa de compressão mais alta devido menor distribuição uniforme dos bits após transformar seus pixels em Bytes. Tanto Babuíno e tanto Lena tiveram taxas mais altas devido sua falta de uniformidade, mas o Babuíno apresenta taxa de compressão maior pois na imagem .PGM P2 dele há mais pixels com representação com mais de 2 bytes (ou seja, o valor é maior que 99).

### Imagem: Quadrado (quadrado_ascii.pgm)
- **Tamanho Original**: 266,112 bytes (260KB)
- **Tamanho Comprimido**: 65,567 bytes (68KB)
- **Taxa de Compressão**: 4.059
- **Análise**: A imagem do quadrado, por ser mais simples e conter grandes áreas uniformes, apresenta uma taxa de compressão menor que a do Babuíno e da Lena. A presença de padrões repetitivos e uniformes permite uma codificação menos eficiente.

### Imagem: Lena (lena_ascii.pgm)
- **Tamanho Original**: 1,228,735 bytes (1.2MB)
- **Tamanho Comprimido**: 262,126 bytes (256MB)
- **Taxa de Compressão**: 4.687
- **Análise**: A imagem da Lena apresenta uma taxa alta em relação ao quadrado pois é menos uniforme, mas menor que o Babuíno, por ter mais pixels escuros (Ou seja, menor que 99).


### Análise Comparativa
- A eficiência da compressão está diretamente relacionada à entropia da imagem, quanto menos uniforme, melhor é a compressão.
- Imagens com pixels mais claros tendem a ter taxas de compressão mais altas.
- O formato PGM ASCII, por sua natureza, já inclui overhead de representação por possuir espaços e quebra de linha.
- A implementação do rescaling garante a estabilidade numérica do processo de codificação.

### Tabela de Resultados da Compressão

| Tamanho Original (bytes) | Tamanho Compactado (bytes) | Imagem Recuperada           | Taxa de Compressão |
|--------------------------|-----------------------------|------------------------------|---------------------|
| 1258676 (1.2M)| 262126 (256K)| recs/baboon_ascii-rec.pgm | 4.806 |
| 266112 (260K)| 65567 (68K)| recs/quadrado_ascii-rec.pgm | 4.059 |
| 1228735 (1.2M)| 262126 (256K)| recs/lena_ascii-rec.pgm | 4.687 |

## Executando os Testes

Para executar todos os testes e gerar as imagens comprimidas e reconstruídas:

```bash
./job.sh
```

### Exemplo de Saída
Ao executar o script, você verá uma saída similar a esta:

```
Original images:
photos/baboon_ascii.pgm: 1258676
photos/lena_ascii.pgm: 1228735
photos/quadrado_ascii.pgm: 266112

Encoded binaries:
bins/baboon_ascii.bin: 262126
bins/lena_ascii.bin: 262126
bins/quadrado_ascii.bin: 65567

Reconstructed images:
recs/baboon_ascii-rec.pgm: 996485
recs/lena_ascii-rec.pgm: 966565
recs/quadrado_ascii-rec.pgm: 241952
```

Note que os arquivos recuperados têm tamanho diferente porque quebras de linha, espaços e comentários são perdidos no processo de otimização, por isso a imagem recuperada tem tamanho menhor.

### Estrutura de Diretórios
- **Imagens originais**: [photos/](photos/)
- **Bitstreams codificados**: [bins/](bins/)
- **Imagens recuperadas**: [recs/](recs/)

### Verificação de Integridade
Após a decodificação, é possível verificar a integridade das imagens comparando os arquivos originais com os reconstruídos,comparando pixel a pixel de cada imagem.

A codificação aritmética implementada garante reconstrução perfeita dos dados originais, sem perda de informação (dos pixels).
