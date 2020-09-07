from yahoo.api import make_request
from nfl.scraper import get_team_stats
from mapping import mapping
import pprint


def rank_defense(oauth, league_id, scoring, debug=0):
    # get list of possible teams
    position_type = "DT"
    position_code = "DEF"
    try:
        teams = make_request(
            oauth, "league/" + league_id + "/players;status=A;position=" + position_code
        )["league"]["players"]["player"]
    except:
        if debug:
            print("Couldn't get teams")
        return
    # score each (filter to the stats that matter. for each stat, do the 2019 calculation)
    relevant_scores = list(
        filter(lambda x: x["position_type"] == position_type, scoring)
    )

    # display_name => {table, column}
    my_mapping = mapping()["Team"]

    # for each player, sum relevant scores
    scored_teams = []
    for team in teams:
        if debug == 2:
            print("Calculating for " + team["editorial_team_full_name"])
        # table_name
        #   year
        #     stat: value
        #     stat: value
        stats = get_team_stats(team["editorial_team_full_name"])
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
                stat = stats.get(map_piece["column"], {})
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
        scored_teams.append(
            {"team": team["editorial_team_full_name"], "score": score,}
        )

    # return by total score
    scored_teams.sort(reverse=True, key=lambda x: x["score"])
    return scored_teams
