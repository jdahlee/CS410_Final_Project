import json
import os
import subprocess

import numpy as np
import pandas as pd

SKIP_PREPROCESSING = True
OVERWRITE_SONG_DOCUMENTS = False

SKIP_INDEXING = False

song_df_columns = [
    "track_name",
    "track_id",
    "artist_names",
    "album_name",
    "duration",
    "release_date",
    "duration_ms",
    "lyrics",
]

doc_ouptut_columns = [
    "track_name",
    "id",
    "artist_names",
    "album_name",
    "duration",
    "release_date",
    "duration_ms",
    "contents",
]


def load_song_data() -> pd.DataFrame:
    song_data_path = "songs.csv"
    song_df = pd.read_csv(song_data_path)

    return song_df


def clean_song_data(song_df: pd.DataFrame) -> pd.DataFrame:
    song_df = (
        song_df.filter(items=song_df_columns)
        .drop_duplicates(subset=["track_id"])
        .dropna(subset=["track_id"])
    )

    song_df = song_df.rename(columns={"lyrics": "contents", "track_id": "id"})
    song_df["contents"] = song_df["contents"].replace(r"^\s*$", np.nan, regex=True)
    song_df = song_df.dropna(subset=["contents"])
    song_df["contents"] = song_df["contents"].str.strip()

    return song_df


def output_song_documents(song_df: pd.DataFrame, output_dir_path: str) -> None:
    os.makedirs(output_dir_path, exist_ok=True)

    failed_songs = []
    for song in song_df.to_dict(orient="records"):
        try:
            song_doc = {}
            for col in doc_ouptut_columns:
                song_doc[col] = song[col]

            song_doc_path = os.path.join(output_dir_path, f"song_{song['id']}.json")
            if not os.path.exists(song_doc_path) or OVERWRITE_SONG_DOCUMENTS:
                with open(song_doc_path, "w", encoding="utf-8") as out:
                    json.dump(
                        song_doc,
                        out,
                        allow_nan=True,
                    )
        except Exception as e:  # noqa: BLE001
            failed_songs.append(
                {"id": song["id"], "track_name": song["track_name"], "exception": e}
            )

    if len(failed_songs) > 0:
        failed_songs_path = "failed_songs"
        with open(failed_songs_path, "w", encoding="utf-8") as file:
            for failed_song in failed_songs:
                file.write(failed_song)
                file.write("\n")

        print(
            f"{len(failed_songs)} songs failed to output, errors written to {failed_songs_path}"
        )


def preprocess_song_data(processed_documents_dir: str) -> None:
    print("loading song data...")
    song_df = load_song_data()
    print("cleaning song data...")
    cleaned_song_df = clean_song_data(song_df)
    print("outputting song documents...")
    output_song_documents(cleaned_song_df, processed_documents_dir)
    print("finsihed preprocessing song documents")


def create_index(input_dir: str, index_dir: str) -> None:
    os.makedirs(index_dir, exist_ok=True)

    cmd = [
        "python",
        "-m",
        "pyserini.index.lucene",
        "--collection",
        "JsonCollection",
        "--input",
        input_dir,
        "--index",
        index_dir,
        "--generator",
        "DefaultLuceneDocumentGenerator",
        "--threads",
        "1",
        "--storePositions",
        "--storeDocvectors",
        "--storeRaw",
    ]
    print(f"Runing subprocess with arguments: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def process_song_data():
    processed_documents_dir = "processed_documents"
    if not SKIP_PREPROCESSING:
        print(f"Preprocessing documents at {processed_documents_dir}")
        preprocess_song_data(processed_documents_dir)

    documents_indexes_dir = "indexes"
    if not SKIP_INDEXING:
        print(f"Indexing documents at {documents_indexes_dir}")
        create_index(input_dir=processed_documents_dir, index_dir=documents_indexes_dir)


if __name__ == "__main__":
    process_song_data()
