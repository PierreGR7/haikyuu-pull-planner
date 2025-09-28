from parameters import gems_per_pull, daily_income, weekly_income, monthly_income, banner_tickets

def calculate_pulls(current_gems: int, current_tickets: int, pity_remaining: int, days_until_banner: int):
    """
    Compute available pulls by the banner end.
    - pity_remaining: how many pulls still needed to reach shop guarantee (e.g., 94 means you need 94 more).
    """
    # 1) Gem income (prorated)
    total_gems = (
        current_gems
        + daily_income * days_until_banner
        + (days_until_banner / 7) * weekly_income
        + (days_until_banner / 31) * monthly_income
    )

    # 2) Pulls from gems (floor)
    pulls_from_gems = int(total_gems // gems_per_pull)

    # 3) Tickets
    pulls_from_tickets = current_tickets
    pulls_from_banner = banner_tickets

    # 4) Totals
    total_pulls = pulls_from_gems + pulls_from_tickets + pulls_from_banner

    return {
        "total_gems": int(total_gems),
        "pulls_from_gems": pulls_from_gems,
        "pulls_from_tickets": pulls_from_tickets,
        "pulls_from_banner": pulls_from_banner,
        "total_pulls": total_pulls,
        "pity_needed": int(pity_remaining),
    }

def is_goal_reached(total_pulls: int, pity_needed: int):
    """
    Compare total pulls with pulls needed to hit pity.
    Returns (goal_reached: bool, remaining_or_surplus: int)
    remaining_or_surplus < 0  -> surplus
    remaining_or_surplus > 0  -> still needed
    """
    goal = total_pulls >= pity_needed
    remaining = pity_needed - total_pulls
    return goal, remaining
