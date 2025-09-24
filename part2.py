import json
from datetime import datetime

# ---------------- Fixture Class ---------------- #
class Fixture:
    def __init__(self, match_id, league, home, away, date_time):
        self.match_id = match_id
        self.league = league
        self.home = home
        self.away = away
        self.date_time = date_time
        self.is_favourite = False

    def __str__(self):
        return f"[{self.league}] {self.date_time.strftime('%d %b %Y %H:%M')} - {self.home} vs {self.away}"

# ---------------- FixtureManager Class ---------------- #
class FixtureManager:
    def __init__(self):
        self.fixtures = []

    def add_fixture(self, fixture):
        self.fixtures.append(fixture)

    def load_from_json(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)
            for row in data:
                match_id = int(row["match_id"])
                league = row["league"]
                home = row["home"]
                away = row["away"]
                # Convert "YYYY-MM-DD HH:MM" string to datetime object
                date_time = datetime.strptime(row["date"], "%Y-%m-%d %H:%M")
                self.add_fixture(Fixture(match_id, league, home, away, date_time))

    def list_leagues(self):
        return sorted(set(f.league for f in self.fixtures))

    def list_teams_in_league(self, league):
        teams = set()
        for f in self.fixtures:
            if f.league.lower() == league.lower():
                teams.add(f.home)
                teams.add(f.away)
        return sorted(teams)

    def fixtures_for_team(self, league, team):
        return [f for f in self.fixtures 
                if f.league.lower() == league.lower() 
                and (f.home.lower() == team.lower() or f.away.lower() == team.lower())]

# ---------------- Main Program ---------------- #
if __name__ == "__main__":
    fm = FixtureManager()
    fm.load_from_json("fixturedata.json")   # <<<<------ CHECK NAME GUYS

    print("⚽ Welcome to Football Fixtures Program ⚽\n")

    while True:
        print("\n===== MAIN MENU =====")
        print("1. Browse Leagues & Teams")
        print("2. View Favourite Teams Inbox")
        print("3. Remove a Team from Favourites")
        print("4. View Fixture Table")   # ⭐ NEW
        print("5. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            leagues = fm.list_leagues()
            print("\nAvailable Leagues:")
            for i, l in enumerate(leagues, start=1):
                print(f"{i}. {l}")

            league_choice = input("\nEnter league name from the list: ").strip()

            if league_choice not in leagues:
                print("❌ Invalid league. Try again.")
                continue

            teams = fm.list_teams_in_league(league_choice)
            print(f"\nTeams in {league_choice}:")
            for t in teams:
                print("-", t)

            team_choice = input("\nEnter team name from the list: ").strip()

            if team_choice not in teams:
                print("❌ Invalid team. Try again.")
                continue

            print(f"\n📅 Fixtures for {team_choice} in {league_choice}:")
            fixtures = fm.fixtures_for_team(league_choice, team_choice)
            for f in fixtures:
                print(f)
