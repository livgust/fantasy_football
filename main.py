from yahoo_oauth import OAuth2
import xmltodict
from yahoo.scoring import scoring
import pprint

league_id = "nfl.l.871073"

oauth = OAuth2(None, None, from_file="yahoo.config.json")

if not oauth.token_is_valid():
    oauth.refresh_access_token()


def make_request(url):
    base_url = "https://fantasysports.yahooapis.com/fantasy/v2/"
    response = oauth.session.get(base_url + url)
    if not response.ok:
        err_text = ""
        err = xmltodict.parse(response.text)
        if "error" in err and "description" in err["error"]:
            err_text = err["error"]["description"]
        return {"error": str(response.status_code) + ": " + err_text}
    else:
        return xmltodict.parse(response.text)["fantasy_content"]


league_scoring = scoring(
    make_request("league/" + league_id + "/settings")["league"]["settings"]
)
pprint.pprint(make_request("league/" + league_id + "/players;status=A"))
