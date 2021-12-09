# Conversor-DOCX-PDF

## Sobre
Ferramenta desenvolvida para fornecer uma interface simples para a conversão em unidade ou em lote de arquivos de imagens ou docx em arquivos pdf.

## Contribuição
Olá, estudo python a quase 1 ano e sou iniciante em github, desenvolvi esse programa para aprender a fazer algo que fosse útil. Consegui, porém o meu código não é dos melhores e precisa de certos ajustes. Criei este repositório para aprender com quem quiser contribuir com o meu código e me ajudar a solucionar alguns problemas nele.



## Dependências

Para o tratamento e converção de imagens instale as libs img2pdf e pillow:

```pip install pillow```

```pip install img2pdf```


Se estiver usando linux instale o abiword:

```sudo apt install abiword```

Para windows, instale docx2pdf:

```pip install docx2pdf```


## pasta_ori e pasta_dest
São diretórios de teste, temos a pasta de origem, onde serão buscados os arquivos e a pasta de destino, onde serão postas as cópias pdf.


## Problemas

**1º- Depende de softwares externos:** A conversão de arquivos docx para pdf em python depende de um software intermediário, como word ou abiword por exemplo. Este código faz uso do abiword pois foi implementado em um sistema linux mint. 

**2º- Compatibilidade:** Este segundo problema foi originado do primeiro. O sistema é compatível com linux, porém por falta de outros sistemas operacionais para testar, não tenho certeza se funciona em algum outro.
