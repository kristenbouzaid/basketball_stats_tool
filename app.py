

# importing raw data
from constants import TEAMS, PLAYERS

# function to clean the list of player data and return it as a new list so original list is left unchanged
def clean_data(PLAYERS):
    cleaned_players = []
    for player in PLAYERS:
        cleaned = {
            "name": player["name"],
            'guardians': player['guardians'].split(" and ")
        }
        if player['experience'] == "YES":
            cleaned['experience'] = True
        else:
            cleaned['experience'] = False
        cleaned["height"] = int(player['height'].split(" ")[0])
        cleaned_players.append(cleaned)
    return cleaned_players

# function to divide up the players into teams with even numbers of players and experience levels
def balance_teams(roster, TEAMS):
    # establishes data set to house all team data for teams once balanced
    balanced_teams = {}
    # establishes the structure within the set for each of the teams
    for team in TEAMS:
        balanced_teams[team] = {
            "total_players": 0,
            "total_experienced": 0,
            "total_inexperienced": 0,
            "total_height": 0,
            "avg_height": 0,
            "player_list_with_height": [],
            "height_sorted_player_list": [],
            "players": [],
            "guardians": []
        }
    # creating a list of inexperienced players and a list of experienced players
    experienced = []
    inexperienced = []
    for player in roster:
        if player['experience'] == True:
            experienced.append(player)
        else:
            inexperienced.append(player)
    # joining the two lists in order so when parsing to teams, the experienced players are distributed first, then the inexperienced players
    players_sorted_by_experience = experienced + inexperienced

    # assigning the players to their teams
    while len(players_sorted_by_experience) > 0:
        for team in TEAMS:
            player_being_assigned = players_sorted_by_experience.pop()
            balanced_teams[team]["total_players"] += 1
            if player_being_assigned["experience"] == True:
                balanced_teams[team]["total_experienced"] += 1
            else:
                balanced_teams[team]["total_inexperienced"] += 1
            balanced_teams[team]["total_height"] += player_being_assigned["height"]
            balanced_teams[team]["avg_height"] = int(balanced_teams[team]["total_height"]/balanced_teams[team]['total_players'])
            balanced_teams[team]["guardians"] += player_being_assigned["guardians"]
            # add the 'popped' player's height and name to the 'player_list_with_height' data field
            balanced_teams[team]["player_list_with_height"].append((player_being_assigned["height"], player_being_assigned["name"]))
            # sorts the names by height and return it to the height_sorted_player_list field
            balanced_teams[team]["height_sorted_player_list"] = sorted(balanced_teams[team]["player_list_with_height"])
            # removes only the name from the sorted list and returns it to the 'players' data field
    # once teams are all assigned, set the players list
    if len(players_sorted_by_experience) == 0:
        for team in TEAMS:
            for entry in balanced_teams[team]["height_sorted_player_list"]:
               balanced_teams[team]["players"].append(entry[1])
    return(balanced_teams)

def display_menu():
    print(f'---- MENU ----\n\n  Here are your choices:\n     A) Display Team Stats\n     B) Quit\n')
    set_of_options = {"A", "B", "a", "b"}
    option = input(f"Enter an option:   ")
    while option not in set_of_options:
        option = input(f"Please enter a valid response. Enter an option:   ")
    return (option.upper())

if __name__ == "__main__":
    # main program code here:
    roster = clean_data(PLAYERS)
    balanced_teams = balance_teams(roster, TEAMS)

    print(f"\nBASKETBALL TEAM STATS TOOL\n")

    option = display_menu()

    while option == "A":
        for number, team in enumerate(TEAMS, start = 1):
            print(f"     {number}. {team}")
        option2 = None
        set_of_options2 = range(0, len(TEAMS))
        while option2 not in set_of_options2:
            try:
                option2 = int(input(f"Enter an option:   ")) - 1
            except IndexError:
                print(f"\nPlease enter a valid number for the chosen team.")
                continue
            except ValueError:
                print(f"\nPlease enter a valid number for the chosen team.")
                continue
            if option2 not in range(0,len(TEAMS)):
                    print(f" \nPlease enter a valid number from the list above.")

        selected_team = TEAMS[option2]
        selected_team_roster = balanced_teams[selected_team]

        print(f"\nStats for the {str(selected_team)}\n-------------------------")
        print(f"Total number of players: {selected_team_roster['total_players']}")
        print(f"Total number of experienced players: {selected_team_roster['total_experienced']}")
        print(f"Total number of inexperienced players: {selected_team_roster['total_inexperienced']}")
        print(f"Average height of the team: {selected_team_roster['avg_height']} inches")

        # this code works for making the player list into a comma separated pretty string
        comma_sep_player_list = (', '.join(selected_team_roster['players']))
        print(f"\nPlayer Names:   {comma_sep_player_list}")

        comma_sep_guardian_list = (', '.join(selected_team_roster['guardians']))
        print(f"\nGuardians of the players: {comma_sep_guardian_list}")

        input("\nTo continue, press ENTER...\n")

        option = display_menu()

    print("\nGoodbye and thanks for using our Basketball Team Stats Tool!")

