# Predição da eficiência de troca térmica

Projeto de Machine Learning para treinar um modelo e prever a eficiência de um trocador de calor.

## Executar localmente

Ative o ambiente virtual e instale as dependências:

```cmd
.venv\Scripts\activate
pip install -r requirements.txt
```

Exemplo de inferência:

```cmd
python src\inference.py --efficiency 10
```

Para consultar as opções:

```cmd
python src\inference.py --help
```

## Docker

O projeto possui imagens separadas para treino e inferência.

### Construir as imagens

Execute na pasta do projeto:

```cmd
docker build -f Dockerfile.train -t docker-ml-projeto-train .
docker build -f Dockerfile.inference -t docker-ml-projeto-inference .
```

### Treinar o modelo

```cmd
docker run --rm -v "%cd%\artifacts:/app/artifacts" docker-ml-projeto-train
```

### Executar inferência

```cmd
docker run --rm docker-ml-projeto-inference --efficiency 10
```

Para estimar o dia a partir de uma eficiência-alvo:

```cmd
docker run --rm docker-ml-projeto-inference --data 95
```

> Os comandos Docker estão documentados, mas ainda não foram testados porque o Docker Engine não está iniciando neste computador.