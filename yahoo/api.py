import xmltodict


def make_request(oauth, url):
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


def get_settings(oauth, league_id):
    return make_request(oauth, "league/" + league_id + "/settings")["league"][
        "settings"
    ]


# position_type = 'O', eligible_positions = [position: QB, position: blah]
# pprint.pprint(make_request("league/" + league_id + "/players;status=A;position=QB"))
