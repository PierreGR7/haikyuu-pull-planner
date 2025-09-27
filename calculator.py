from datetime import datetime

def calculate_pulls(current_gems, gems_per_pull, daily_income, current_tickets, days_until_banner):
    """ Calculate the number of pulls needed to reach the target gems and tickets """
    total_gems = current_gems + daily_income * days_until_banner
    pulls_from_gems = total_gems // gems_per_pull
    total_pulls = current_tickets + pulls_from_gems
    return total_pulls
    
def is_goal_reached(total_pulls, target_pulls):
    is_reached = total_pulls >= target_pulls
    left_pulls = target_pulls - total_pulls
    return is_reached, left_pulls


