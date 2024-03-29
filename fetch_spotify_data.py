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
