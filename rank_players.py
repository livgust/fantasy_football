from yahoo.api import make_request
from nfl.scraper import get_player_stats
from mapping import mapping
import pprint


def rank_players(oauth, league_id, position, scoring, debug=0):
    # get list of possible players
    position_code = position["position"]
    position_type = position["position_type"]
    if debug >= 2:
        print("Ranking players of position " + position_code)
    try:
        position_query = (
            "position=" + position_code
            if position_code != "W/R/T"
            else "position=WR;position=TE;position=RB"
        )
        players = []
        req_count = 25
        next_req_start = 0
        while req_count == 25:
            url = "league/" + league_id + "/players;status=A;"
            if next_req_start > 0:
                url += "start=" + str(next_req_start) + ";"
            url += position_query
            req = make_request(oauth, url)["league"]["players"]
            req_count = int(req["@count"]) if req and "@count" in req else 0
            if req_count:
                players.extend(req["player"])
            next_req_start += req_count
    except Exception as e:
        if debug:
            print("Could not rank players of position " + position_code)
            print(e)
            raise e
        return
    # score each (filter to the stats that matter. for each stat, do the 2019 calculation)
    relevant_scores = list(
        filter(lambda x: x["position_type"] == position_type, scoring)
    )

    # display_name => {table, column}
    my_mapping = mapping()["Individual"]

    # for each player, sum relevant scores
    scored_players = []
    # TODO: get rid of "JR" and "III," etc. Also make things like "J.J." change to "j-j"
    for player in players:
        if debug >= 2:
            print("Calculating for " + player["name"]["full"])
        # table_name
        #   year
        #     stat: value
        #     stat: value
        stats = get_player_stats(player["name"]["first"], player["name"]["last"])
        if not stats:
            if debug:
                print("No stats found for " + player["name"]["full"])
            continue
        games_mapping = my_mapping.get("Season Games")
        season_games = (
            stats.get(list(stats.keys())[0], {})  # grab any table
            .get("2019", {})
            .get(games_mapping["column"], "")
        ) or "0"
        season_games = int(season_games)
        if not season_games:
            if debug >= 2:
                print("  No games.")
            continue
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
                if stat and "parse" in map_piece:  # specially parse out the stat
                    stat = map_piece["parse"](stat)
                if stat:
                    if debug == 3:
                        print("  stat is " + stat)
                    # multiply and add
                    score += float(stat) * float(relevant_score["value"])
                else:
                    if debug >= 2:
                        print(
                            "  couldn't calculate stat for "
                            + relevant_score["display_name"]
                        )
            else:
                if debug >= 2:
                    print(
                        "  don't know how to translate "
                        + relevant_score["display_name"]
                    )
            if debug == 3:
                print("  score is now " + str(score))
        if debug >= 2:
            print("  done calculating.")
        scored_players.append(
            {
                "player": player["name"]["first"] + " " + player["name"]["last"],
                "score": score / season_games,
            }
        )

    # return by total score
    scored_players.sort(reverse=True, key=lambda x: x["score"])
    return scored_players[:20]  # return only highest 20 ranked
