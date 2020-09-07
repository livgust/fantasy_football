from yahoo.api import make_request
from nfl.scraper import get_player_stats
from mapping import mapping
import pprint


def rank_players(oauth, league_id, position, scoring, debug=0):
    # get list of possible players
    position_code = position["position"]
    position_type = position["position_type"]
    if debug == 2:
        print("Ranking players of position " + position_code)
    try:
        players = make_request(
            oauth, "league/" + league_id + "/players;status=A;position=" + position_code
        )["league"]["players"]["player"]
    except:
        if debug:
            print("Could not rank players of position " + position_code)
        return
    # score each (filter to the stats that matter. for each stat, do the 2019 calculation)
    relevant_scores = list(
        filter(lambda x: x["position_type"] == position_type, scoring)
    )

    # display_name => {table, column}
    my_mapping = mapping()["Individual"]

    # for each player, sum relevant scores
    scored_players = []
    for player in players:
        if debug == 2:
            print("Calculating for " + player["name"]["full"])
        # table_name
        #   year
        #     stat: value
        #     stat: value
        stats = get_player_stats(player["name"]["first"], player["name"]["last"])
        score = 0
        #   id
        #   display_name
        #   name
        #   position_type
        #   value
        for relevant_score in relevant_scores:
            if debug == 3:
                print("  adding score for " + relevant_score["display_name"])
            # link relevant_score to stat
            map_piece = my_mapping.get(relevant_score["display_name"])
            # pprint.pprint(map_piece)
            if map_piece:
                stat = (
                    stats.get(map_piece["table"], {})
                    .get("2019", {})
                    .get(map_piece["column"])
                )
                if stat:
                    if debug == 3:
                        print("  stat is " + stat)
                    # multiply and add
                    score += float(stat) * float(relevant_score["value"])
                else:
                    if debug:
                        print(
                            "  couldn't calculate stat for "
                            + relevant_score["display_name"]
                        )
            else:
                if debug:
                    print(
                        "  don't know how to translate "
                        + relevant_score["display_name"]
                    )
            if debug == 3:
                print("  score is now " + str(score))
        if debug == 2:
            print("  done calculating.")
        scored_players.append(
            {
                "player": player["name"]["first"] + " " + player["name"]["last"],
                "score": score,
            }
        )

    # return by total score
    scored_players.sort(reverse=True, key=lambda x: x["score"])
    return scored_players
