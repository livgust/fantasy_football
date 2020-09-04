def mapping():
    return {
        "Rush TD": {"table": "Rushing", "column": "TD"},
        "Rec": {"table": "Receiving", "column": "REC"},
        "Rec Yds": {"table": "Receiving", "column": "YDS"},
        "Rec TD": {"table": "Receiving", "column": "TD"},
        "Ret TD": {"table": "Kick Return", "column": "TD"},
        "2-PT": {},  # dunno where this is
        "Fum Lost": {"table": "Fumbles", "column": "LOST"},
        "FG 0-19": {"table": "Kicking", "column": "1-19"},  # completed-attempted
        "FG 20-29": {"table": "Kicking", "column": "20-29"},  # completed-attempted
        "FG 30-39": {"table": "Kicking", "column": "30-39"},  # completed-attempted
        "FG 40-49": {"table": "Kicking", "column": "40-49"},  # completed-attempted
        "FG 50+": {"table": "Kicking", "column": "50+"},  # completed-attempted
        "PAT Made": {},  # dunno where this is
        "Sack": {"column": "SACKS"},
        # TODO: on-purpose dupe
        # "Int": {},  # would have to aggregate
        "Fum Rec": {},  # would have to aggregate
        "TD": {
            "column": "TOUCHDOWNS (Rushing - Passing - Returns - Defensive)"
        },  # need to parse out
        "Safe": {},  # would have to aggregate
        "Blk Kick": {},  # would have to aggregate
        "Pass Yds": {"table": "Passing", "column": "YDS"},
        # TODO: DUPLICATE but probably on purpose
        # "Ret TD": {
        #    "column": "TOUCHDOWNS (Rushing - Passing - Returns - Defensive)"
        # },  # need to parse out,
        "Pass TD": {"table": "Passing", "column": "TD"},
        "Pts Allow 0": {},
        "Pts Allow 1-6": {},
        "Pts Allow 7-13": {},
        "Pts Allow 14-20": {},
        "Pts Allow 21-27": {},
        "Pts Allow 28-34": {},
        "Pts Allow 35+": {},
        "Fum Ret TD": {"table": "Fumbles", "column": "OWN FR"},
        "Int": {"table": "Passing", "column": "INT"},
        "XPR": {},
        "Rush Yds": {"table": "Rushing", "column": "YDS"},
    }