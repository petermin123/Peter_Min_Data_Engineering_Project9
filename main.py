import pandas as pd
from matplotlib import pyplot as plt
from ydata_profiling import ProfileReport


def read_spotify_data(filename):
    return pd.read_csv(filename, encoding="latin-1")


def generate_summary_stats(df: pd.DataFrame):
    return df.describe()


def generate_summary_for_stream_count():
    df = read_spotify_data("spotify-2023.csv")

    df["streams"] = pd.to_numeric(df["streams"], errors="coerce")
    df.dropna(subset=["streams"], inplace=True)

    stream_median = df["streams"].median()
    stream_max = df["streams"].max()
    stream_min = df["streams"].min()
    return (stream_median, stream_max, stream_min)


def generate_markdown():
    info1, info2, info3 = generate_summary_for_stream_count()
    info1 = str(info1)
    info2 = str(info2)
    info3 = str(info3)

    with open("stream_count_summary.md", "w", encoding="utf-8") as file:
        file.write("Median:\n")
        file.write(info1)
        file.write("\n\n")
        file.write("Max:\n")
        file.write(info2)
        file.write("\n\n")
        file.write("Min:\n")
        file.write(info3)


def generate_reports(df: pd.DataFrame):
    profile = ProfileReport(df, title="Spotify Streaming Data 2023")
    profile.to_file("spotify_data.html")


def generate_bar_chart_for_most_popular_artists(df: pd.DataFrame):
    df["streams"] = pd.to_numeric(df["streams"], errors="coerce")
    df.dropna(subset=["streams"], inplace=True)

    # Create bar chart for 10 hottest songs reflected in stream counts
    top_artists = df.groupby("artist(s)_name")["streams"].sum().nlargest(10)
    plt.figure(figsize=(10, 6))
    top_artists.plot(kind="bar", color="blue")
    plt.title("10 Hottest Artists by Total Stream Count")
    plt.xlabel("Artists")
    plt.ylabel("Total Streams")
    plt.xticks(rotation=45)
    plt.show()


def main():
    spotify_df = read_spotify_data("spotify-2023.csv")
    summary_stats = generate_summary_stats(spotify_df)
    print(summary_stats)

    generate_markdown()
    generate_reports(spotify_df)
    generate_bar_chart_for_most_popular_artists(spotify_df)


if __name__ == "__main__":
    main()
