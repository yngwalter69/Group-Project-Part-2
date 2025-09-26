import json
from datetime import datetime
import os
# ---------------- Fixture Class ---------------- #
class Fixture:
    def __init__(self, match_id, league, home, away, date_time):
        self.match_id = match_id
        self.league = league
        self.home = home
        self.away = away
        self.date_time = date_time

    def __str__(self):
        return f"[{self.league}] {self.date_time.strftime('%d %b %Y %H:%M')} - {self.home} vs {self.away}"

# ---------------- FixtureManager Class ---------------- #
class FixtureManager:
    def __init__(self):
        self.fixtures = []
        self.favourite_teams = set()

    def add_fixture(self, fixture):
        self.fixtures.append(fixture)

    def load_from_json(self, filename):
        if not os.path.exists(filename):
            print(f"❌ File '{filename}' not found.")
            return
        
        try: 
            with open(filename, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print(f"⚠️ File '{filename}' is empty or contains invalid JSON.")
            return
        except Exception as e:
            print(f"⚠️ Unexpected error reading '{filename}': {e}")
            return
        
        for row in data:
            try:
                match_id = int(row["match_id"])
                league = row["league"]
                home = row["home"]
                away = row["away"]
                date_time = datetime.strptime(row["date"], "%Y-%m-%d %H:%M")
                self.add_fixture(Fixture(match_id, league, home, away, date_time))
            except (KeyError, ValueError) as e:
                print(f"⚠️ Skipping invalid fixture: {e}")   

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
    
    # -------- FAVOURITES ----------- #
    def add_favourite_team(self, team):
        self.favourite_teams.add(team)

    def remove_favourite_team(self, team):
        if team in self.favourite_teams:
            self.favourite_teams.remove(team)
            return True
        return False

    def list_favourite_fixtures(self):
        return [f for f in self.fixtures 
                if f.home in self.favourite_teams or f.away in self.favourite_teams]

    def save_favourites(self, filename="favourites.json"):
        try:
            with open(filename, "w") as f:
                json.dump(list(self.favourite_teams), f, indent=4)
            print(f"Favourites saved to '{filename}'.")
        except (IOError, OSError) as e:
            print(f"Failed to save favourites to '{filename}':{e}")

    def load_favourites(self, filename="favourites.json"):
        if os.path.exists(filename):
            with open(filename, "r") as f:
                try:
                    data = json.load(f)
                    self.favourite_teams = set(data)
                except json.JSONDecodeError:
                    print("⚠️ Favourites file is empty or corrupted.")
    
    def search_fixtures(self, keyword):
        return [
            f for f in self.fixtures
            if keyword.lower() in f.home.lower()
            or keyword.lower() in f.away.lower()
            or keyword.lower() in f.league.lower()
            ]

# ---------------- Main Program ---------------- #
if __name__ == "__main__":
    fm = FixtureManager()
    fm.load_from_json("fixturedata.json")   # <<<<------ CHECK NAME GUYS
    fm.load_favourites("favourites.json")   # <<<<------ CHECK NAME GUYS

    print("⚽ Welcome to Football Fixtures Program ⚽\n")

    while True:
        print("\n===== MAIN MENU =====")
        print("1. Browse Leagues & Teams")
        print("2. Search fixtures by keyword")
        print("3. View Favourite Teams Inbox")
        print("4. Remove a Team from Favourites")
        print("5. View Fixture Table")   # ⭐ NEW
        print("6. Exit")

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
            fav_choice = input("\nDo you want to add this team to your favourites? (yes/no): ").strip().lower()
            if fav_choice == "yes":
                fm.add_favourite_team(team_choice)
                fm.save_favourites("favourites.json")
                print(f"⭐ {team_choice} added to favourites!")

        elif choice == "2":   
            keyword = input("\nEnter keyword of name to search (team or league): ").strip()
            results = fm.search_fixtures(keyword)

            if not results:
                print(f"❌ No fixtures found for '{keyword}'.")
            else:
                print(f"\n🔍 Search Results for '{keyword}':")
                print("-" * 70)
                print(f"{'Match ID':<10} {'League':<15} {'Date':<20} {'Fixture'}")
                print("-" * 70)
                
                for f in results:
                    print(f"{f.match_id:<10} {f.league:<15} {f.date_time.strftime('%d %b %Y %H:%M'):<20} {f.home} vs {f.away}")
                    print("-"*70)
        
        elif choice == "3":
            if not fm.favourite_teams:
                print("\n📭 Your favourites inbox is empty!")
            else:
                print("\n⭐ Favourite Teams:")
                for t in fm.favourite_teams:
                    print("-", t)

                print("\n📌 Fixtures for Favourite Teams:")
                for f in fm.list_favourite_fixtures():
                    print(f)
        
        elif choice == "4":
            if not fm.favourite_teams:
                print("\n📭 You have no favourites to remove!")
            else:
                print("\n⭐ Current Favourite Teams:")
                for t in fm.favourite_teams:
                    print("-", t)

                team_remove = input("\nEnter the team name you want to remove: ").strip()
                if fm.remove_favourite_team(team_remove):
                    fm.save_favourites("favourites.json")
                    print(f"🗑 {team_remove} removed from favourites.")
                else:
                    print("❌ That team is not in your favourites.")

        elif choice == "5":   # ⭐ Fixture Table
            print("\n📅 FIXTURE TABLE 📅")

            print("\nSort Options:")
            print("1. By Date (default)")
            print("2. By League")
            print("3. By Team (Home team alphabetical)")

            sort_choice = input("\nEnter sort choice (1/2/3): ").strip()

            if sort_choice == "2":
                fixtures_sorted = sorted(fm.fixtures, key=lambda x: x.league.lower())
            elif sort_choice == "3":
                fixtures_sorted = sorted(fm.fixtures, key=lambda x: x.home.lower())
            else:
                fixtures_sorted = sorted(fm.fixtures, key=lambda x: x.date_time)


            print("-" * 70)
            print(f"{'Match ID':<10} {'League':<15} {'Date':<20} {'Fixture'}")
            print("-" * 70)
            for f in fixtures_sorted:
                print(f"{f.match_id:<10} {f.league:<15} {f.date_time.strftime('%d %b %Y %H:%M'):<20} {f.home} vs {f.away}")
            print("-" * 70)
        
        elif choice == "6":
            print("\n👋 Goodbye! Thanks for using the Fixtures Program.")
            break

        else:
            print("❌ Invalid choice, please try again.")