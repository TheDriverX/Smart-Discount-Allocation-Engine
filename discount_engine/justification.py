def generate_justification(agent, amount, score, values):
    remarks = []

    perf = agent["performanceScore"]
    tenure = agent["seniorityMonths"]
    achievement = agent["targetAchievedPercent"]
    clients = agent["activeClients"]

    # Evaluate performance score
    max_perf = max(values["performanceScore"])
    if perf >= 0.9 * max_perf:
        remarks.append("exceptional performance")
    elif perf >= 0.75 * max_perf:
        remarks.append("strong performance")

    # Evaluate seniority
    max_tenure = max(values["seniorityMonths"])
    if tenure > 0 and tenure >= 0.9 * max_tenure:
        remarks.append("long-standing service")
    elif tenure <= 0.2 * max_tenure:
        remarks.append("new to the team")

    # Target achievement assessment
    max_achievement = max(values["targetAchievedPercent"])
    if achievement > 0 and achievement >= 0.9 * max_achievement:
        remarks.append("impressive target completion")

    # Active client handling
    max_clients = max(values["activeClients"])
    if clients > 0 and clients >= 0.9 * max_clients:
        remarks.append("handles a large client base")

    # Default fallback message
    if not remarks:
        remarks.append("consistent overall contribution")

    remarks[0] = remarks[0].capitalize()
    return " and ".join(remarks)
