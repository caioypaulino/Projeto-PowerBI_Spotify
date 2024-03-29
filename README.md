# **Projeto: Relatório Dashboard - Spotify (Power BI, PowerPoint e Python)**

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

## PowerPoint
A ferramenta Microsoft PowerPoint foi utilizada nesse projeto para criação do Background que foi escolhido para o layout do Dashboard.<br>
Ele foi modelado a partir de formas e estilos personalizados na plataforma, segue a imagem do resultado final:<br><br>
![Background](/pptx/Background.png)

## Power BI (Insights e DAX)
Alguns dos Insights gerados a partir das medidas criadas utilizando funções DAX: <br>
- Average Stream per Year:<br>
![Average Stream per Year I](/img/Average%20Stream%20per%20Year%20Insight.png)<br>
![Average Stream per Year](/img/Average%20Stream%20per%20Year.png)


- Top Song vs AVG (+Val):<br>
![Top Song vs AVG I](/img/Top%20Song%20vs%20AVG%20Insight.png)<br>
![Top Song vs AVG Val](/img/Top%20Song%20vs%20AVG%20Val.png)
![Top Song vs AVG](/img/Top%20Song%20vs%20AVG.png)


- Track Count:<br>
![Track Count I](/img/Track%20Count%20Insight.png)<br>
![Track Count](/img/Track.png)

- Percent Val:<br>
![Percent Val I](/img/Percent%20Val%20Insight.png)<br>
![Percent Val](/img/Percent%20Val.png)

- Image HTML:<br>
![Image HTML I](/img/Image%20HTML%20Insight.png)<br>
![Image HTML](/img/Image%20HTML.png)

## Extra Visuals
Vale citar o uso de visuais personalizados que foram baixados como conteúdo extra no Power BI para auxiliar no processo de análise.

- **Deneb: Declarative Visualization**<br>
Este visual foi responsável pela criação de gráficos customizados a partir de Templates, assim como o Heat Map personalizado de "Track Count", já citado anteriormente. Derivado de Template registrado no seguinte repositório github: https://github.com/PowerBI-tips/Deneb-Templates/blob/main/templates/heatmap%20with%20bars%20-%20red%20themed.json.<br>
Também possibilitou a criação da KPI "Percent Val" já citada, através do Template: https://github.com/PBI-David/Deneb-Showcase.

- **HTML Content**<br>
Este visual tornou possível utilizar códigos HTML no Power BI. Dessa forma foi realizada a exibição do Album Cover de cada música no visual de "Image HTML" registrado na seção anterior de Insights.

## Dashboard
Aqui está a estrutura final do painel de Dashboard criado no Power BI, construído a partir das análises e gráficos:

![DashboardGif](/img/Dashboard.gif)
![DashboardJpg](/img/Spotify%20Dashboard.jpg)