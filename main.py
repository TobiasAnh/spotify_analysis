from funcs import *


def main():
    # Credentials
    sp = getSpotipyCredentials()

    # =============================================================================
    # Test with podcasts
    # =============================================================================

    showId = "7BTOsF2boKmlYr76BelijW"
    # show = getShowInformation(sp, showId)
    episodes = getEpisodeInformation(sp, showId)
    episodes.to_csv(f"episodes.csv")


if __name__ == "__main__":
    main()
