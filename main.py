from yahoo_oauth import OAuth2
from yahoo.scoring import scoring
from yahoo.api import get_settings
from rank_players import rank_players
from rank_defense import rank_defense
import json

league_id = "nfl.l.871073"

oauth = OAuth2(None, None, from_file="yahoo.config.json")

if not oauth.token_is_valid():
    oauth.refresh_access_token()

settings = get_settings(oauth, league_id)

roster_positions = settings["roster_positions"]["roster_position"]
# BN is bench, IR is injured reserve, DEF is defense

league_scoring = scoring(settings)

# for each position, get list of possible players and rank by points
final_rankings = {}

for position in roster_positions:
    if (position["position"] == "IR") or (position["position"] == "BN"):
        continue
    elif position["position"] == "DEF":
        final_rankings[position["position"]] = {
            "count": position["count"],
            "rankings": rank_defense(oauth, league_id, league_scoring, debug=1),
        }
    else:
        final_rankings[position["position"]] = {
            "count": position["count"],
            "rankings": rank_players(
                oauth, league_id, position, league_scoring, debug=1
            ),
        }

with open("out.json", "w") as outfile:
    json.dump(final_rankings, outfile, indent=4)
