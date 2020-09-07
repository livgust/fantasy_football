from bs4 import BeautifulSoup
import requests
import pprint


def get_player_stats(first_name, last_name):  # names are LC
    stats = {}

    base_url = "https://www.nfl.com/players/"
    end_url = "/stats/"
    complete_url = (
        base_url
        + first_name.lower().replace(" ", "-")
        + "-"
        + last_name.lower().replace(" ", "-")
        + end_url
    )
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

    # table_name
    #   year
    #     stat: value
    #     stat: value
    return stats


def get_team_stats(team_name):  # team name is LC with dashes
    stats = {}

    base_url = "https://www.nfl.com/teams/"
    end_url = "/stats/"
    complete_url = base_url + team_name.lower().replace(" ", "-") + end_url
    page = requests.get(complete_url)
    soup = BeautifulSoup(page.content)

    li_stats = soup.find("div", class_="nfl-c-team-stats").find_all("li")
    for li in li_stats:
        # TODO: FIRST DOWNS, PASSING, OFFENSE, RUSHING, TOUCHDOWNS(),
        label = ""
        if li.find(class_="nfl-o-team-h2h-stats__label--full"):
            label = li.find(class_="nfl-o-team-h2h-stats__label--full").get_text(
                strip=True
            )
        else:
            label = li.find(class_="nfl-o-team-h2h-stats__label").get_text(strip=True)
        stats[label] = li.find(class_="nfl-o-team-h2h-stats__value").get_text(
            strip=True
        )

    pprint.pprint(stats)
    return stats
