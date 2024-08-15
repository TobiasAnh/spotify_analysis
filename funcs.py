import json
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv


def getSpotipyCredentials():

    # Strava API ids
    CLIENT_ID = os.getenv("ClientId")
    CLIENT_SECRET = os.getenv("ClientSecret")

    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError("Missing CLIENT_ID or CLIENT_SECRET in environment variables")

    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET
        )
    )

    return sp


def getShowInformation(sp, showId):
    show = sp.show(
        showId,
        market="de",
    )

    return show


def getEpisodeInformation(sp, showId):
    limit_reached = False
    offset = 0
    df = pd.DataFrame()

    while not limit_reached:
        shows = sp.show_episodes(
            showId,
            limit=50,
            offset=offset,
            market="de",
        )

        episodeId = []
        name = []
        release_date = []
        duration_min = []
        description = []
        link = []

        for episode in shows["items"]:
            episodeId.append(episode["id"])
            release_date.append(episode["release_date"])
            name.append(episode["name"])
            duration_min.append(episode["duration_ms"] / 1000 / 60)
            description.append(episode["description"])
            link.append(episode["external_urls"]["spotify"])

        _ = pd.DataFrame(
            {
                "episodeId": episodeId,
                "release_date": release_date,
                "name": name,
                "duration_min": duration_min,
                "description": description,
                "link": link,
            }
        )

        df = pd.concat([df, _], axis=0)

        offset = offset + 50
        if len(df) == shows["total"]:
            break

    df = df.set_index("episodeId")

    return df


def createJson(dictionary, file_path):
    with open(file_path, "w") as json_file:
        json.dump(dictionary, json_file, indent=4)
