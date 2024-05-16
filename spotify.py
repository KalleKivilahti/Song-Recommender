import customtkinter
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pygame
import requests
import tempfile

client_id = '00a9521c5d544c4ea183a9a71b9c3541'
client_secret = '4ba57571ed6945d8ac24dc36d549bd06'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

pygame.mixer.init()

root = customtkinter.CTk()
root.geometry("900x1000")

frame = customtkinter.CTkScrollableFrame(root, orientation="vertical", width=800, height=900)
frame.pack(pady=40)

def get_recommendations(event=None):

    query = entry1.get()
    
    for widget in frame.winfo_children()[3:]:
        widget.destroy()

    def search(query):
        track_results = sp.search(q='track:' + query, type='track', limit=1)
        artist_results = sp.search(q='artist:' + query, type='artist', limit=1)
        
        if track_results['tracks']['items']:
            return track_results['tracks']['items'][0]
        elif artist_results['artists']['items']:
            return artist_results['artists']['items'][0]
        else:
            print("No results found.")
            return None
    
    def fetch_recommendations():
        result = search(query)
        if result:
            if 'name' in result:
                if result['type'] == 'track':
                    recommendation_label = customtkinter.CTkLabel(master=frame, text=f"{result['name']} by {result['artists'][0]['name']}")
                    recommendation_label.pack(pady=5, padx=20)
                    recommendations = sp.recommendations(seed_tracks=[result['id']], limit=20)
                    for idx, track in enumerate(recommendations['tracks'], start=1):
                        recommendation_label = customtkinter.CTkLabel(master=frame, text=f"{idx}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}")
                        recommendation_label.pack(pady=5, padx=20)
                        play_button = customtkinter.CTkButton(master=frame, text="Play", command=lambda url=track['preview_url']: play_song(url))
                        play_button.pack(pady=5, padx=20)
                        stop_button = customtkinter.CTkButton(master=frame, text="Stop", command=stop_song)
                        stop_button.pack(pady=5, padx=20)
                elif result['type'] == 'artist':
                    print("Fetching artist recommendations...")
            else:
                print("Result type not supported.")
    
    fetch_recommendations()

def play_song(preview_url):
    if preview_url:
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
            response = requests.get(preview_url)
            tmp_file.write(response.content)
            tmp_file.close()
            pygame.mixer.music.load(tmp_file.name)
            pygame.mixer.music.play()
    else:
        print("Preview URL not found for this track.")

def stop_song():
    pygame.mixer.music.stop()

root.bind("<Return>", get_recommendations)

label = customtkinter.CTkLabel(master=frame, text="Music Recommendations")
label.pack(pady=50, padx=40)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Track name: ")
entry1.pack(pady=30, padx=20)

button = customtkinter.CTkButton(master=frame, text="Get recommendations", command=get_recommendations)
button.pack(pady=30, padx=20)

root.bind("<Return>", get_recommendations)

root.mainloop()