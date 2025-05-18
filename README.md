# Codificador Aritmético

Esse trabalho implementa um codificador e decodificador aritmético binário com suporte a *rescaling* para evitar underflow.

# Uso

## Codificar

```bash
python3 encoder.py in.pgm out.bin
```

O arquivo `in.pgm` será lido, seus dados serão codificados com compressão aritmética binária e o resultado será salvo em `out.bin`, contendo os metadados e o bitstream comprimido.

## Decodificar

```bash
python3 decoder.py out.bin new-in.pgm
```

O arquivo `out.bin` será decodificado e a imagem original será reconstruída e salva como `new-in.pgm`.


# Experimento

Para executar os testes e obter os arquivos compactados e reconstruídos, basta rodar:

```bash
./job.sh
```

## Resultados

- **Imagens originais**: [photos/](photos/)
- **Bitstreams codificados**: [bins/](bins/)
- **Imagens recuperadas**: [recs/](recs/)

### Tabela de Compressão


| Tamanho Original (bytes) | Tamanho Compactado (bytes) | Imagem Recuperada           | Taxa de Compressão |
|--------------------------|-----------------------------|------------------------------|---------------------|
| 1258676 (1.2M)| 1107545 (1.1M)| recs/baboon_ascii-rec.pgm | 0.880 |
| 266112 (260K)| 241564 (236K)| recs/quadrado_ascii-rec.pgm | 0.908 |
| 1228735 (1.2M)| 1078483 (1.0M)| recs/lena_ascii-rec.pgm | 0.878 |
