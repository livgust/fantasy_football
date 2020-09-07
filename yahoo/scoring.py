def scoring(stats):
    # stat:
    #   stat_id: 56
    #   enabled: 1
    #   name: Points Allowed 35+ points
    #   display_name: Pts Allow 35+
    #   sort_order: 1
    #   position_type: DT
    categories = stats["stat_categories"]["stats"]["stat"]

    # stat:
    #   stat_id: 4
    #   value: 0.04
    modifiers = stats["stat_modifiers"]["stats"]["stat"]
    grouped_modifiers = {}
    for modifier in modifiers:
        grouped_modifiers[modifier["stat_id"]] = modifier["value"]

    complete_stats = []
    for category in categories:
        if category["enabled"] and not (  # if enabled and not a display stat
            "is_only_display_stat" in category and category["is_only_display_stat"]
        ):
            complete_stats.append(
                {
                    "id": category["stat_id"],
                    "name": category["name"],
                    "display_name": category["display_name"],
                    "position_type": category["position_type"],
                    "value": grouped_modifiers[str(category["stat_id"])],
                }
            )

    #   id
    #   display_name
    #   name
    #   position_type
    #   value
    return complete_stats
