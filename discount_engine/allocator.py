import math
from .justification import generate_justification
from .utils import normalize, distribute_leftover

def allocate_discounts(site_kitty, sales_agents, config=None):
    config = config or {}

    # Extract weightage for different metrics
    weights = config.get("weights", {
        "performanceScore": 1.0,
        "seniorityMonths": 1.0,
        "targetAchievedPercent": 1.0,
        "activeClients": 1.0
    })

    # Derive min and max allocation limits (as absolute or % of total kitty)
    min_alloc = config.get("min_allocation_amount", 0)
    max_alloc = config.get("max_allocation_amount", float('inf'))

    if "min_allocation_percent" in config:
        min_alloc = max(min_alloc, config["min_allocation_percent"] * site_kitty)
    if "max_allocation_percent" in config:
        max_alloc = min(max_alloc, config["max_allocation_percent"] * site_kitty)

    use_base_allocation = config.get("use_base_allocation", False)
    base_percent = config.get("base_allocation_percent", 0.0)

    agent_count = len(sales_agents)
    allocation_map = {agent['id']: 0 for agent in sales_agents}

    # Distribute base allocation if enabled
    total_base = base_percent * site_kitty if use_base_allocation else 0
    if total_base and agent_count:
        per_agent_base = total_base / agent_count
        for agent in sales_agents:
            allocation_map[agent['id']] = per_agent_base

    remaining_budget = site_kitty - total_base

    # Normalize each attribute for all agents
    features = ["performanceScore", "seniorityMonths", "targetAchievedPercent", "activeClients"]
    raw_values = {feature: [agent[feature] for agent in sales_agents] for feature in features}
    normalized_scores = {feature: normalize(values) for feature, values in raw_values.items()}

    # Compute weighted score per agent
    agent_scores = {}
    for index, agent in enumerate(sales_agents):
        score = sum(
            weights[feature] * normalized_scores[feature][index]
            for feature in features
        )
        agent_scores[agent['id']] = score

    total_score = sum(agent_scores.values())

    # Distribute remaining kitty based on scores
    if total_score > 0:
        for agent in sales_agents:
            agent_id = agent['id']
            share = agent_scores[agent_id] / total_score
            allocation_map[agent_id] += share * remaining_budget
    else:
        # If all scores are zero, split equally
        fallback_share = remaining_budget / agent_count if agent_count else 0
        for agent in sales_agents:
            allocation_map[agent['id']] += fallback_share

    # Enforce min and max constraints iteratively
    adjustment_needed = True
    while adjustment_needed:
        adjustment_needed = False
        for agent in sales_agents:
            agent_id = agent['id']
            current = allocation_map[agent_id]

            if current < min_alloc:
                deficit = min_alloc - current
                allocation_map[agent_id] = min_alloc
                per_other_loss = deficit / (agent_count - 1)
                for other in sales_agents:
                    if other['id'] != agent_id:
                        allocation_map[other['id']] -= per_other_loss
                adjustment_needed = True
                break

            if current > max_alloc:
                surplus = current - max_alloc
                allocation_map[agent_id] = max_alloc
                per_other_gain = surplus / (agent_count - 1)
                for other in sales_agents:
                    if other['id'] != agent_id:
                        allocation_map[other['id']] += per_other_gain
                adjustment_needed = True
                break

    # Round down values and distribute any leftover
    for agent_id in allocation_map:
        allocation_map[agent_id] = math.floor(allocation_map[agent_id])

    allocation_map = distribute_leftover(
        allocation_map, agent_scores, total_score, site_kitty
    )

    # Build final structured output
    output = {"allocations": []}
    for agent in sales_agents:
        agent_id = agent['id']
        output["allocations"].append({
            "id": agent_id,
            "assignedDiscount": int(allocation_map[agent_id]),
            "justification": generate_justification(
                agent,
                allocation_map[agent_id],
                agent_scores[agent_id],
                raw_values
            )
        })

    return output
