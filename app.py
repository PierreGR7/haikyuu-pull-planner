import json
from datetime import datetime
from calculator import calculate_pulls, is_goal_reached
from parameters import daily_income, weekly_income, monthly_income, gems_per_pull, banner_tickets

# Load JSON data
with open("DATA/incoming_banner.json", "r") as f:
    banners = json.load(f)

print("=== Upcoming Banners ===")
today = datetime.today().date()

# Get only future banners
upcoming_banners = [
    (b["character"], datetime.fromisoformat(b["start_date"]).date(), datetime.fromisoformat(b["end_date"]).date(), b["is_rerun"])
    for b in banners
    if datetime.fromisoformat(b["end_date"]).date() >= today
]

# Display future banners
for i, (char, start, end, rerun) in enumerate(upcoming_banners, 1):
    r_flag = " (Rerun)" if rerun else ""
    print(f"{i}. {char}{r_flag} — {start} → {end}")

choice = int(input("\nSelect the number of the banner you are aiming for: "))
target_char, start_date, end_date, _ = upcoming_banners[choice - 1]
days_until_banner = (end_date - today).days

# COUNT banners from now to target banner (inclusive)
banner_count = choice  # because our list is sorted and 1-indexed
total_banner_tickets = banner_count * banner_tickets

print(f"\n🎯 Selected Banner: {target_char} (ends on {end_date}, in {days_until_banner} days)")
print(f"⚙️  Current Config: {daily_income}/day | {weekly_income}/week | {monthly_income}/month | {banner_tickets} tickets per banner | {gems_per_pull} gems/pull")
print(f"   (Banners until target: {banner_count}, so total banner tickets = {total_banner_tickets})\n")

# User inputs
current_gems = int(input("💎 Current gems: "))
current_tickets = int(input("🎟️ Current UR tickets: "))
pity_remaining = int(input("📊 Pity remaining (how many pulls left for guarantee): "))

# Pass total banner tickets to the calculator
result = calculate_pulls(current_gems, current_tickets, pity_remaining, days_until_banner)
result["pulls_from_banner"] = total_banner_tickets
result["total_pulls"] = result["pulls_from_gems"] + result["pulls_from_tickets"] + result["pulls_from_banner"]

goal_reached, remaining_pulls = is_goal_reached(result["total_pulls"], result["pity_needed"])

# Display results
print(f"\n📊 Results:")
print(f"   ➤ Total predicted gems: {result['total_gems']}")
print(f"   ➤ Pulls from gems: {result['pulls_from_gems']}")
print(f"   ➤ Current UR tickets: {result['pulls_from_tickets']}")
print(f"   ➤ Banner tickets (all banners): {result['pulls_from_banner']}")
print(f"   ➤ Total available pulls: {result['total_pulls']}")
print(f"   ➤ Pulls needed for pity: {result['pity_needed']}")

if goal_reached:
    print(f"✅ Goal reached! Surplus: {abs(remaining_pulls)} pulls")
else:
    print(f"❌ Not enough... you still need {abs(remaining_pulls)} pulls")
