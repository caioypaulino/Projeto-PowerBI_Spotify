# **Projeto: Análise de BI - Spotify (Power BI, PowerPoint e Python)**

## **Stack**
Power BI, PowerPoint, Python(pandas, requests)

## **Sobre**
Projeto de análise e visualização de dados, importando um dataset Kaggle, enriquecendo dados com consumo da API Spotify via Python e exportando os dados para um Dashboard Interativo gerado no Power BI.

## **Sobre os Dados**
Os dados foram retirados do seguinte Dataset Kaggle: https://www.kaggle.com/datasets/nelgiriyewithana/top-spotify-songs-2023.

## Sobre o Dataset
Este Dataset contém uma lista abrangente das músicas mais famosas de 2023 listadas no Spotify.

### Os campos incluem:

- track_name: Nome da música
- artist(s)name: Nome do(s) artista(s) da música
- artist_count: Número de artistas que contribuem para a música
- released_year: Ano em que a música foi lançada
- released_month: Mês em que a música foi lançada
- released_day: Dia do mês em que a música foi lançada
- in_spotify_playlists: Número de playlists do Spotify em que a música está incluída
- in_spotify_charts: Presença e classificação da música nos rankings do Spotify
- streams: Número total de streams no Spotify
- in_apple_playlists: Número de playlists do Apple Music em que a música está incluída
- in_apple_charts: Presença e classificação da música nos rankings do Apple Music
- in_deezer_playlists: Número de playlists do Deezer em que a música está incluída
- in_deezer_charts: Presença e classificação da música nos rankings do Deezer
- in_shazam_charts: Presença e classificação da música nos rankings do Shazam
- bpm: Batidas por minuto, uma medida do ritmo da música
- key: Tonalidade da música
- mode: Modo da música (maior ou menor)
- danceability%: Percentual que indica o quão adequada a música é para dançar
- valence_%: Positividade do conteúdo musical da música
- energy_%: Nível de energia percebido da música
- acousticness_%: Quantidade de som acústico na música
- instrumentalness_%: Quantidade de conteúdo instrumental na música
- liveness_%: Presença de elementos de performance ao vivo
- speechiness_%: Quantidade de palavras faladas na música
  
> Existem 953 registros.

## Python
Para que as músicas possuíssem suas respectivas imagens de capa do álbum (album cover), foi utilizado o script Python abaixo para extrair cada imagem via API do Spotify e inserir nas respectivas linhas do DataFrame pandas.

``` python
import requests
import pandas as pd


# GET Spotify Token
def get_spotify_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'

    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })

    auth_data = auth_response.json()

    return auth_data['access_token']


# Procurando por uma track(faixa) e buscando ID
def search_track(track_name, artist_name, token):
    query = f"{track_name} artist:{artist_name}"
    url = f"https://api.spotify.com/v1/search?q={query}&type=track"

    response = requests.get(url, headers={
        'Authorization': f'Bearer {token}'
    })

    json_data = response.json()

    try:
        first_result = json_data['tracks']['items'][0]
        track_id = first_result['id']

        return track_id
    except (KeyError, IndexError):
        return None


# GET track details (detalhes da faixa)
def get_track_details(track_id, token):
    url = f"https://api.spotify.com/v1/tracks/{track_id}"

    response = requests.get(url, headers={
        'Authorization': f'Bearer {token}'
    })

    json_data = response.json()

    image_url = json_data['album']['images'][0]['url']

    return image_url


# Spotidy API Credentials
client_id = 'xxxxxxxxxxxxxx' # Foi necessário censurar o token
client_secret = 'xxxxxxxxxxxxxx' # Foi necessário censurar o token

# GET Token
access_token = get_spotify_token(client_id, client_secret)

# Criando DataFrame a partir do arquivo .csv
df_spotify = pd.read_csv('spotify-2023.csv', encoding='ISO-8859-1')

# Looping passando por cada linha do DataFrame obtendo imagem de cada track(faixa)
for i, row in df_spotify.iterrows():
    track_id = search_track(row['track_name'], row['artist_name'], access_token)
    print("Counter: ", i)

    if track_id:
        image_url = get_track_details(track_id, access_token)

        df_spotify.at[i, 'image_url'] = image_url

# Salvando o DataFrame atualizado, exportando em .csv
df_spotify.to_csv('updated_spotify_data.csv', index=False)
```

## Power BI (DAX)
Algumas das medidas criadas utilizando funções DAX:
Average Stream per Year 


## Dashboard
Aqui está a estrutura final do painel de Dashboard, construído a partir das análises e gráficos criados através do Databricks Notebook:

![DashboardGif](https://github.com/caioypaulino/Projeto-Videogame_Sales_Databricks/blob/main/Images/Dashboard.gif)

## Imagens de Exemplo:
(Acesse o link acima para conferir todas as análises detalhadas)

![Dashboard](https://github.com/caioypaulino/Projeto-Videogame_Sales_Databricks/blob/main/Images/Dashboard%20Videogame%20Sales%20Example.png)

![Notebook5](https://github.com/caioypaulino/Projeto-Videogame_Sales_Databricks/blob/main/Images/Notebook%20005%20Example.png)

![Notebook6](https://github.com/caioypaulino/Projeto-Videogame_Sales_Databricks/blob/main/Images/Notebook%20006%20Example.png)
