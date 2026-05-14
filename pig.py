def pig_botmove(points, roll_score):
    if roll_score + points >= 100:
        return "BANK"
    if roll_score <= 25:
        return "RISK"
    else:
        return "BANK"