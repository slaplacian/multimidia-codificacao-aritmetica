# Codificador Aritmético

Este projeto implementa um codificador e decodificador aritmético binário com suporte a *rescaling* para evitar underflow. A codificação aritmética é um método de compressão de dados que representa uma sequência de símbolos como um único número racional entre 0 e 1.

## Requisitos

- Python 3.x
- Biblioteca `bitstring`

## Uso

### Codificar uma Imagem

Para codificar uma imagem PGM, use o comando:

```bash
python3 encoder.py photos/lena_ascii.pgm bins/lena_ascii.bin
```

O arquivo de entrada será lido, seus dados serão codificados com compressão aritmética binária e o resultado será salvo em um arquivo binário contendo os metadados e o bitstream comprimido.

### Decodificar uma Imagem

Para decodificar o arquivo binário e recuperar a imagem original:

```bash
python3 decoder.py bins/lena_ascii.bin recs/lena_ascii-rec.pgm
```

## Exemplos

O projeto inclui três imagens de exemplo para demonstração:

1. **Lena** (1.2MB)
   - Original: `photos/lena_ascii.pgm`
   - Comprimido: `bins/lena_ascii.bin`
   - Recuperado: `recs/lena_ascii-rec.pgm`

2. **Baboon** (1.2MB)
   - Original: `photos/baboon_ascii.pgm`
   - Comprimido: `bins/baboon_ascii.bin`
   - Recuperado: `recs/baboon_ascii-rec.pgm`

3. **Quadrado** (260KB)
   - Original: `photos/quadrado_ascii.pgm`
   - Comprimido: `bins/quadrado_ascii.bin`
   - Recuperado: `recs/quadrado_ascii-rec.pgm`

## Executando os Testes

Para executar todos os testes e gerar os arquivos compactados e reconstruídos automaticamente:

```bash
./job.sh
```

## Resultados da Compressão

| Imagem | Tamanho Original | Tamanho Compactado | Taxa de Compressão |
|--------|------------------|-------------------|-------------------|
| Lena | 1.2MB | 1.0MB | 0.878 |
| Baboon | 1.2MB | 1.1MB | 0.880 |
| Quadrado | 260KB | 236KB | 0.908 |

## Estrutura do Projeto

- `photos/`: Contém as imagens PGM originais
- `bins/`: Armazena os arquivos binários comprimidos
- `recs/`: Contém as imagens reconstruídas após decodificação
- `encoder.py`: Implementação do codificador aritmético
- `decoder.py`: Implementação do decodificador aritmético
- `job.sh`: Script para executar todos os testes

## Detalhes Técnicos

O codificador utiliza uma implementação de 32 bits com suporte a rescaling para evitar underflow. O processo de codificação inclui:

1. Cálculo das frequências dos símbolos
2. Codificação aritmética com rescaling
3. Geração do bitstream final

O arquivo de saída contém:
- Número total de bits
- Contagem de zeros e uns
- Bitstream comprimido
