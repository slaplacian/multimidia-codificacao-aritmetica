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
- **Tamanho Comprimido**: 1,107,545 bytes (1.1MB)
- **Taxa de Compressão**: 1.136
- **Análise**: A imagem do babuíno apresenta uma taxa de compressão moderada devido à sua complexidade e detalhes. A presença de texturas e padrões complexos resulta em uma distribuição mais uniforme dos símbolos, limitando a eficiência da compressão aritmética.

### Imagem: Quadrado (quadrado_ascii.pgm)
- **Tamanho Original**: 266,112 bytes (260KB)
- **Tamanho Comprimido**: 241,564 bytes (236KB)
- **Taxa de Compressão**: 1.102
- **Análise**: A imagem do quadrado, por ser mais simples e conter grandes áreas uniformes, apresenta uma taxa de compressão ligeiramente melhor que a do babuíno. A presença de padrões repetitivos permite uma codificação mais eficiente.

### Imagem: Lena (lena_ascii.pgm)
- **Tamanho Original**: 1,228,735 bytes (1.2MB)
- **Tamanho Comprimido**: 1,078,483 bytes (1.0MB)
- **Taxa de Compressão**: 1.139
- **Análise**: A imagem Lena apresenta a melhor taxa de compressão entre as três imagens testadas. Isso se deve à sua combinação de áreas suaves e detalhes bem definidos, que resultam em uma distribuição de símbolos mais favorável para a codificação aritmética.

### Análise Comparativa
- A eficiência da compressão está diretamente relacionada à entropia da imagem
- Imagens com maior complexidade e detalhes tendem a ter taxas de compressão mais altas
- O formato PGM ASCII, por sua natureza, já inclui overhead de representação que limita a eficiência da compressão
- A implementação do rescaling garante a estabilidade numérica do processo de codificação

### Tabela de Resultados da Compressão

| Tamanho Original (bytes) | Tamanho Compactado (bytes) | Imagem Recuperada           | Taxa de Compressão |
|--------------------------|-----------------------------|------------------------------|---------------------|
| 1258676 (1.2M)| 1107545 (1.1M)| recs/baboon_ascii-rec.pgm | 1.136 |
| 266112 (260K)| 241564 (236K)| recs/quadrado_ascii-rec.pgm | 1.102 |
| 1228735 (1.2M)| 1078483 (1.0M)| recs/lena_ascii-rec.pgm | 1.139 |

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
bins/baboon_ascii.bin: 1107545
bins/lena_ascii.bin: 1078483
bins/quadrado_ascii.bin: 241564

Reconstructed images:
recs/baboon_ascii-rec.pgm: 1258676
recs/lena_ascii-rec.pgm: 1228735
recs/quadrado_ascii-rec.pgm: 266112
```

Note que os arquivos reconstruídos têm exatamente o mesmo tamanho dos originais, confirmando que a codificação aritmética é um método de compressão sem perdas.

### Estrutura de Diretórios
- **Imagens originais**: [photos/](photos/)
- **Bitstreams codificados**: [bins/](bins/)
- **Imagens recuperadas**: [recs/](recs/)

### Verificação de Integridade
Após a decodificação, é possível verificar a integridade das imagens comparando os arquivos originais com os reconstruídos:

```bash
diff photos/lena_ascii.pgm recs/lena_ascii-rec.pgm
```

A codificação aritmética implementada garante reconstrução perfeita dos dados originais, sem perda de informação.
