<h1 align="center"> Spotify API </h1>

<p align="center">Este repositório contém o 1º desafio da mentoria individual do <a href="https://desenvolve.grupoboticario.com.br/">Programa Desenvolve 2023 - Trilha Dados</a>. O desafio se tratou do desenvolvimento de um <strong>ETL</strong> simples, onde se buscou <strong>extrair, processar e carregar</strong> dados da API pública do Spotify em um banco de dados Postgresql, usando a linguagem Python. <p>
<p align="center">
    <a href="##Executar projeto">Executar projeto</a> |
    <a href="##Desafio">Desafio</a> |
    <a href="##Tecnologias">Tecnologias</a> |
    <a href="##Dados">Dados</a> |
    <a href="##Projeto">Projeto</a>
</p>


## Executar projeto

Para instalar as bibliotecas necessárias para executar este projeto, deve ser usado o arquivo [`requirements.txt`](https://github.com/Vinicius999/Desafio-01-Mentor-Spotify-API/blob/main/requirements.txt). Para fazer isso, abra o terminal, navegue até a pasta do seu priojeto e execute o seguinte comando:

```
pip install -r requirements.txt
```

Feito isso, podemos executar o arquivo [`main.py`](https://github.com/Vinicius999/Desafio-01-Mentor-Spotify-API/blob/main/main.py) usando o comando:

```
python3 main.py
```

## Desafio

1. Utilizar Python para ler dados da [API do Spotify](https://developer.spotify.com/documentation/web-api/tutorials/getting-started) e encontrar episódios onde a palavra "Python" aparecer.

2. Armazenar no banco de dados as seguintes informações:
    - id do episodio;
    - descrição;
    - link;
    - lista de imagens

3. Baixar as imagens dos eposódios a partir da lista de imagens gravadas no banco de dados e gravar em uma pasta dentro do projeto;

#### Pontos analisados:

- Padronização do código;
- Identação;
- Versionamento;
- Programação Orientada a Objetos

## Tecnologias

<p style='margin: 16px 4px 32px;'>
    <a href="https://www.python.org/" target="_blank" rel="noopener noreferrer">
        <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" alt="Vini-python" width="40" height="40" />
    </a>
	<a href="https://pandas.pydata.org/" target="_blank" rel="noreferrer">
        <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original-wordmark.svg" alt="Vini-streamlit" width="40" height="40" />
    </a>
</p>

## Dados

- Fonte dos dados: [Spotify API](https://developer.spotify.com/)

- Documentação: [documentação](https://developer.spotify.com/documentation/web-api)

## Projeto

Para se conectar e ler dados da API do Spotify, foi desenvolvida a classe `Spotipy`, contendo as funções de altenticação e busca de espisódios usando a biblioteca [spotipy](https://spotipy.readthedocs.io/en/2.22.1/):

```python
class Spotipy():
    def __init__ (self, CLIENT_ID, CLIENT_SECRET):
        self.CLIENT_ID = CLIENT_ID
        self.CLIENT_SECRET = CLIENT_SECRET
    
    def authentication(self):
        auth_manager = SpotifyClientCredentials(
            client_id = self.CLIENT_ID,
            client_secret = self.CLIENT_SECRET
        )

        self.sp = spotipy.Spotify(auth_manager = auth_manager)
        return self.sp

    def get_all_episodes_with_python(self, sp):
        self.episodes = []
        self.offset = 0
        self.limit = 50  # max limit
        self.market='BR' 
        
        while True:
            self.results = sp.search(q='Python', type='episode', limit=self.limit, offset=self.offset, market=self.market)
            self.episodes += self.results['episodes']['items']
            self.offset += self.limit
            if len(self.results['episodes']['items']) == 0:
                break  
        return self.episodes
```



<h4 align="center"> &#128679; README.md &#128640; em construção... &#128679; </h4>
