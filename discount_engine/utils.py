def normalize(values):
    """
    Scale a list of numeric values between 0 and 1 based on the maximum value.
    If the list is empty or the max value is 0, all entries are treated as 0.
    """
    max_value = max(values) if values else 1
    if max_value == 0:
        max_value = 1
    return [v / max_value for v in values]


def distribute_leftover(allocations, scores, total_score, total_kitty):
    """
    Distribute any remaining undistributed amount (due to flooring) to agents
    proportionally based on their score rankings.
    """
    remainder = total_kitty - sum(allocations.values())

    if remainder <= 0:
        return allocations

    # Rank agent IDs by score in descending order
    ranked_agents = sorted(scores.keys(), key=lambda agent_id: scores[agent_id], reverse=True)

    index = 0
    while remainder > 0:
        agent_id = ranked_agents[index % len(ranked_agents)]
        allocations[agent_id] += 1
        remainder -= 1
        index += 1

    return allocations
