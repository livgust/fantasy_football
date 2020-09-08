from bs4 import BeautifulSoup
import requests
import json
import os.path

import pprint


def get_player_stats(first_name, last_name):  # names are LC
    stats = {}

    complete_name = (
        first_name.lower().replace(" ", "-") + "-" + last_name.lower().replace(" ", "-")
    )
    file_name = "./cache_stats/individual/" + complete_name + ".json"

    if os.path.isfile(file_name):
        with open(file_name) as file:
            return json.load(file)

    base_url = "https://www.nfl.com/players/"
    end_url = "/stats/"
    complete_url = base_url + complete_name + end_url
    page = requests.get(complete_url)
    soup = BeautifulSoup(page.content)

    tables = soup.find_all("div", class_="nfl-t-stats--table")
    for table in tables:
        child = table.find("div", class_="nfl-o-roster")
        if child:
            table_title = child.find("div", class_="nfl-t-stats__title").get_text(
                strip=True
            )
            stats[table_title] = {}

            stats_table = child.find("table")
            headers = list(
                map(lambda th: th.get_text(strip=True), stats_table.find_all("th"))
            )
            for row in stats_table.tbody.find_all("tr"):
                row_data = list(
                    map(lambda td: td.get_text(strip=True), row.find_all("td"))
                )
                year = ""
                row_dict = {}
                for index, data in enumerate(row_data):
                    if index == 0:
                        year = row_data[index]  # year should be the "group by"
                    else:
                        row_dict[headers[index]] = data
                stats[table_title][year] = row_dict

    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, "w") as outfile:
        json.dump(stats, outfile)
    # table_name
    #   year
    #     stat: value
    #     stat: value
    return stats


def get_team_stats(team_name, team_abbr):  # team name is LC with dashes
    stats = {}
    formatted_team_name = team_name.lower().replace(" ", "-")
    file_name = "./cache_stats/team/" + formatted_team_name + ".json"
    formatted_team_abbr = team_abbr.lower()

    if os.path.isfile(file_name):
        with open(file_name) as file:
            return json.load(file)

    base_url = "https://www.nfl.com/teams/"
    end_url = "/stats/"
    complete_url = base_url + formatted_team_name + end_url
    page = requests.get(complete_url)
    soup = BeautifulSoup(page.content)

    li_stats = soup.find("div", class_="nfl-c-team-stats").find_all("li")
    for li in li_stats:
        label = ""
        if li.find(class_="nfl-o-team-h2h-stats__label--full"):
            label = li.find(class_="nfl-o-team-h2h-stats__label--full").get_text(
                strip=True
            )
        else:
            label = li.find(class_="nfl-o-team-h2h-stats__label").get_text(strip=True)

        # some labels should return arrays as they contain multiple stats
        if label == "TOUCHDOWNSRushingPassingReturnsDefensive":
            stats[label] = list(
                map(
                    lambda x: x.get_text(strip=True),
                    li.find(class_="nfl-o-team-h2h-stats__value").find_all("span"),
                )
            )
        stats[label] = li.find(class_="nfl-o-team-h2h-stats__value").get_text(
            strip=True
        )

    supp_page = requests.get(
        "https://www.espn.com/nfl/team/stats/_/type/team/name/" + formatted_team_abbr
    )
    supp_soup = BeautifulSoup(supp_page.content)
    supp_metrics = ["Total Points Per Game", "Interceptions", "Fumbles-Lost"]
    for supp_metric in supp_metrics:
        index = supp_soup.find("tr", string=supp_metric).get("data-idx")
        raw_value = (
            supp_soup.find_all(attrs={"data-idx": index})[-1]
            .find_all("td")[-1]
            .get_text(strip=True)
        )
        stats[supp_metric] = raw_value

    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, "w") as outfile:
        json.dump(stats, outfile)
    return stats
