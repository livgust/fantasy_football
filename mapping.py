def mapping():
    number_of_games = 16
    return {
        "Individual": {
            "Rush TD": {"table": "Rushing", "column": "TD"},
            "Rec": {"table": "Receiving", "column": "REC"},
            "Rec Yds": {"table": "Receiving", "column": "YDS"},
            "Rec TD": {"table": "Receiving", "column": "TD"},
            "Ret TD": {"table": "Kick Return", "column": "TD"},
            "2-PT": {},  # dunno where this is. RARE
            "Fum Lost": {"table": "Fumbles", "column": "LOST"},
            "FG 0-19": {
                "table": "Kicking",
                "column": "1-19",
                "parse": lambda x: x[: x.index("-")],
            },  # completed-attempted
            "FG 20-29": {
                "table": "Kicking",
                "column": "20-29",
                "parse": lambda x: x[: x.index("-")],
            },  # completed-attempted
            "FG 30-39": {
                "table": "Kicking",
                "column": "30-39",
                "parse": lambda x: x[: x.index("-")],
            },  # completed-attempted
            "FG 40-49": {
                "table": "Kicking",
                "column": "40-49",
                "parse": lambda x: x[: x.index("-")],
            },  # completed-attempted
            "FG 50+": {
                "table": "Kicking",
                "column": "50+",
                "parse": lambda x: x[: x.index("-")],
            },  # completed-attempted
            "PAT Made": {},  # dunno where this is
            "Pass Yds": {"table": "Passing", "column": "YDS"},
            "Pass TD": {"table": "Passing", "column": "TD"},
            "Fum Ret TD": {"table": "Fumbles", "column": "TD"},
            "Int": {"table": "Passing", "column": "INT"},
            "Rush Yds": {"table": "Rushing", "column": "YDS"},
        },
        "Team": {
            "Sack": {"column": "SACKS"},
            "Int": {"column": "Interceptions"},
            "Fum Rec": {
                "column": "Fumbles-Lost",
                "parse": lambda x: x[x.index("-") + 1 :],
            },
            "TD": {
                "column": "TOUCHDOWNSRushingPassingReturnsDefensive",
                "parse": lambda x: x[3],
            },
            "Safe": {},  # would have to aggregate. RARE
            "Blk Kick": {},  # would have to aggregate. Kinda Rare
            "Ret TD": {
                "column": "TOUCHDOWNSRushingPassingReturnsDefensive",
                "parse": lambda x: x[2],
            },
            "Pass TD": {"table": "Passing", "column": "TD"},
            "Pts Allow 0": {
                "column": "Total Points Per Game",
                "parse": lambda x: number_of_games if float(x) < 1 else 0,
            },
            "Pts Allow 1-6": {
                "column": "Total Points Per Game",
                "parse": lambda x: number_of_games
                if float(x) >= 1 and float(x) < 7
                else 0,
            },
            "Pts Allow 7-13": {
                "column": "Total Points Per Game",
                "parse": lambda x: number_of_games
                if float(x) >= 7 and float(x) < 14
                else 0,
            },
            "Pts Allow 14-20": {
                "column": "Total Points Per Game",
                "parse": lambda x: number_of_games
                if float(x) >= 14 and float(x) < 21
                else 0,
            },
            "Pts Allow 21-27": {
                "column": "Total Points Per Game",
                "parse": lambda x: number_of_games
                if float(x) >= 21 and float(x) < 28
                else 0,
            },
            "Pts Allow 28-34": {
                "column": "Total Points Per Game",
                "parse": lambda x: number_of_games
                if float(x) >= 28 and float(x) < 35
                else 0,
            },
            "Pts Allow 35+": {
                "column": "Total Points Per Game",
                "parse": lambda x: number_of_games if float(x) >= 35 else 0,
            },
            "XPR": {},  # RARE
        },
    }
