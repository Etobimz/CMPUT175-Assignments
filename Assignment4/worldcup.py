import random
from linkedlist import LinkedListNode, LinkedListt, MatchHistoryNode, MatchHistoryLinkedList


def initialize_teams(csv_file):
    """
    Read teams from a CSV file and return both a list of all teams and linked lists for each group.

    Parameters:
        csv_file (str): Path to the CSV file.

    Returns:
        list: A list of all team names.
        list: A list of linked lists, where each linked list contains teams in a group.
    """
    all_teams = []  #  list of all team names
    Teams_in_group = []  # List to store linked lists for each group
    try:
        with open(csv_file, 'r') as file:
            lines = file.readlines()

            if len(lines) < 2:
                raise ValueError("CSV file is empty or does not contain enough data.")

            group_teams = {}
            for line in lines[1:]: # Skip the header line
                parts = line.strip().split(',')
                if len(parts) == 3:
                    group, team, power = parts
                    all_teams.append(team)

                    if group not in group_teams:
                        group_teams[group] = LinkedListt()

                    team_data = {
                        "name": team, "power": int(power), "points": 0,
                        "wins": 0, "losses": 0, "draws": 0, "GD": 0
                    }
                    group_teams[group].append_team(team_data)
                else:
                    print(f"Skipping malformed line: {line.strip()}")

            Teams_in_group.extend(group_teams.values())

    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        return [], [] # Return empty lists on error
    except ValueError as e:
        print(f"Error: {e}")
        return [], [] # Return empty lists on error

    return all_teams, Teams_in_group



def simulate_match(team1, team2, match_history, game_number):
    """
    Simulates a match between two teams and updates the match history.
    """
    # Use scaled goals to keep scores realistic
    goal_range = max(1, abs(team1["power"] - team2["power"]) // 2)
    team1_goals = random.randint(0, goal_range)
    team2_goals = random.randint(0, goal_range)

    # Determine match outcome
    if team1_goals > team2_goals:
        team1["points"] += 3
        team1["wins"] += 1
        team2["losses"] += 1
    elif team2_goals > team1_goals:
        team2["points"] += 3
        team2["wins"] += 1
        team1["losses"] += 1
    else:
        team1["points"] += 1
        team2["points"] += 1
        team1["draws"] += 1
        team2["draws"] += 1

    # Update GD directly here
    team1["GD"] += (team1_goals - team2_goals)
    team2["GD"] += (team2_goals - team1_goals)

    # Add match to history
    match_history.add_match(game_number, team1["name"], team2["name"], team1_goals, team2_goals)

    return team1, team2




def group_match_play(team1, team2):
    """
    Simulates a group stage match between two teams.

    Parameters:
        team1 (dict): Data for the first team.
        team2 (dict): Data for the second team.

    Returns:
        tuple: Updated data for both teams.
    """
    team1_goals = random.randint(0, team1["power"])
    team2_goals = random.randint(0, team2["power"])

    if team1_goals > team2_goals:
        team1["points"] += 3
        team1["wins"] += 1
        team2["losses"] += 1
    elif team2_goals > team1_goals:
        team2["points"] += 3
        team2["wins"] += 1
        team1["losses"] += 1
    else:
        team1["points"] += 1
        team2["points"] += 1
        team1["draws"] += 1
        team2["draws"] += 1

    team1["GD"] += (team1_goals - team2_goals)
    team2["GD"] += (team2_goals - team1_goals)

    return team1, team2



def group_update_after_match(group, team1_name, team2_name, team1_goals, team2_goals):
    current = group.head
    while current:
        team = current.get_data()
        if team["name"] == team1_name:
            team["GD"] += (team1_goals - team2_goals)
            if team1_goals > team2_goals:
                team["points"] += 3
                team["wins"] += 1
            elif team1_goals == team2_goals:
                team["points"] += 1
                team["draws"] += 1
            else:
                team["losses"] += 1
            current.set_data(team)
        elif team["name"] == team2_name:
            team["GD"] += (team2_goals - team1_goals)
            if team2_goals > team1_goals:
                team["points"] += 3
                team["wins"] += 1
            elif team1_goals == team2_goals:
                team["points"] += 1
                team["draws"] += 1
            else:
                team["losses"] += 1
            current.set_data(team)
        current = current.get_next()




def group_stage_matches(groups, match_history):
    """
    Simulates group stage matches for all groups and tracks match history.

    Parameters:
        groups (list): A list of LinkedListt objects, each representing a group.
        match_history (MatchHistoryLinkedList): The linked list to store match history.

    Returns:
        list: The updated LinkedListt objects after the group stage.
    """
    game_number = 1  # Initialize game number for tracking
    for group_index, group in enumerate(groups):
        #print(f"\nSimulating matches for Group {chr(65 + group_index)}:")

        current_node = group.head
        while current_node:
            opponent_node = current_node.get_next()
            while opponent_node:
                team1_data = current_node.get_data()
                team2_data = opponent_node.get_data()

                # Simulate a match and update match history
                updated_team1, updated_team2 = simulate_match(
                    team1_data.copy(), team2_data.copy(), match_history, game_number
                )
                game_number += 1

                # Update the group after the match
                group_update_after_match(group, updated_team1["name"], updated_team2["name"], 
                                         updated_team1["GD"], updated_team2["GD"])

                opponent_node = opponent_node.get_next()
            current_node = current_node.get_next()

        # Sort group standings
        group.sort(key=lambda x: (x["points"], x["GD"], x["power"]), reverse=True)

    return groups



def display_group_rankings(groups): 
    """Displays rankings for all groups."""
    for i, group in enumerate(groups):
        group_name = chr(ord('A') + i) # Get group name (A, B, C, etc.)
        print(f"\nRankings for Group {group_name}:")
        group.display_rankings() # Call display_rankings on each group (LinkedListt)




def promote_teams(groups):
    """
    Identifies the top two teams from each group and promotes them to the next stage.
    Eliminates the other teams from the linked lists.

    Parameters:
        groups (list): A list of LinkedListt objects, each representing a group of teams.

    Returns:
        list: A list of dictionaries, where each dictionary represents a qualified team.
    """
    qualified_teams = []

    for group_index, group_list in enumerate(groups):
        print(f"\nProcessing Group {chr(65 + group_index)}")

        # Sort the group by points, goal difference, then power (important!)
        group_list.sort(key=lambda x: (x["points"], x["GD"], x["power"]), reverse=True) 

        # Promote top 2 teams
        current = group_list.head
        for _ in range(2):
            if current:
                qualified_teams.append(current.get_data().copy()) # Append copy to avoid unintended modification
                current = current.get_next()

        # Remove the bottom two teams (correctly):
        while group_list.size() > 2: # Adjust this as per number of teams to eliminate.
            group_list.delete(group_list.get_tail().get_data()["name"]) # Delete by name from the tail end

        print(f"Qualified teams from Group {chr(65 + group_index)}:")
        for team in qualified_teams[-2:]:
            print(f"{team['name']} with {team['points']} points") 

    return qualified_teams


def setup_knockout_round(groups):
    """
    Selects the top two teams from each group and creates the knockout linked list.

    Parameters:
        groups (list): A list of LinkedListt objects representing the groups.

    Returns:
        LinkedListt: A linked list of teams in the knockout stage.
    """
    knockout_list = LinkedListt()

    for group in groups:
        # Sort the group by points (descending)
        group.sort(key=lambda team: team["points"], reverse=True)
        current = group.head
        count = 0

        # Add top 2 teams to the knockout list
        while current and count < 2:
            knockout_list.append_team(current.get_data())
            current = current.get_next()
            count += 1

    return knockout_list


def knockout_match_play(team1, team2):
        """
        Simulates a knockout match between two teams. No ties are allowed.

        Parameters:
        team1 (dict): Data for the first team.
        team2 (dict): Data for the second team.

        Returns:
        tuple: Winning and losing team data.
        """
        while True:  # Ensure no ties
            team1_goals = random.randint(0, team1["power"])
            team2_goals = random.randint(0, team2["power"])

            if team1_goals > team2_goals:
                return team1, team2
            elif team2_goals > team1_goals:
                return team2, team1


def knockout_update_after_match(knockout_list, losing_team_name):
        """
        Removes the losing team from the knockout linked list.

        Parameters:
        knockout_list (LinkedListt): The linked list of teams in the knockout round.
        losing_team_name (str): Name of the team that lost the match.
        """
        knockout_list.delete(losing_team_name)


def play_knockout_round(knockout_list, match_history):
    """
        Plays a single knockout round and updates the list.

        Parameters:
        knockout_list (LinkedListt): The linked list of teams in the knockout round.
        match_history (MatchHistoryLinkedList): Linked list to store match history.
        
    
    """
    current = knockout_list.head
    game_number = match_history.size + 1

    while current and current.get_next():
        team1 = current.get_data()
        team2 = current.get_next().get_data()

        # Simulate the match
        winner, loser = knockout_match_play(team1, team2)
        print(f"{winner['name']} defeated {loser['name']}")

        # Add the match result to history
        match_history.add_match(game_number, winner["name"], loser["name"], 
                                winner["power"], loser["power"])
        game_number += 1

        # Remove the losing team from the list
        knockout_update_after_match(knockout_list, loser["name"])

        # Move to the next match pair
        current = knockout_list.head  # Start from the head after modifying the lis
        

def single_day_group_matches(groups, match_history):
    """
    Simulates a single day of group stage matches.

    Parameters:
        groups (list): A list of LinkedListt objects, each representing a group.
        match_history (MatchHistoryLinkedList): The match history tracker.

    Returns:
        None
    """
    for group_index, group in enumerate(groups):
        print(f"\nSimulating matches for Group {chr(65 + group_index)}:")

        games_played = 0
        current = group.head
        while current and games_played < 2:  # Limit to 2 matches per group
            opponent = current.get_next()
            while opponent and games_played < 2:
                team1 = current.get_data()
                team2 = opponent.get_data()

                # Simulate match
                updated_team1, updated_team2 = group_match_play(team1.copy(), team2.copy())
                
                # Add match to history
                match_history.add_match(match_history.size + 1, team1["name"], team2["name"], 
                                        updated_team1["GD"], updated_team2["GD"])

                # Update standings
                group_update_after_match(group, team1["name"], team2["name"], 
                                         updated_team1["GD"], updated_team2["GD"])

                games_played += 1
                opponent = opponent.get_next()
            current = current.get_next()

        # Sort group standings after matches
        group.sort(key=lambda x: (x["points"], x["GD"], x["power"]), reverse=True)


def single_day_knockout_matches(knockout_list, match_history):
    """
    Simulates a single day of knockout stage matches.

    Parameters:
        knockout_list (LinkedListt): The linked list of teams in the knockout round.
        match_history (MatchHistoryLinkedList): The match history tracker.

    Returns:
        None
    """
    current = knockout_list.head
    game_number = match_history.size + 1

    print("\nKnockout Matches:")
    while current and current.get_next():
        team1 = current.get_data()
        team2 = current.get_next().get_data()

        # Simulate the match
        winner, loser = knockout_match_play(team1, team2)
        print(f"{winner['name']} defeated {loser['name']}")

        # Add the match to history
        match_history.add_match(game_number, winner["name"], loser["name"], 0, 0)
        game_number += 1

        # Remove losing team
        knockout_update_after_match(knockout_list, loser["name"])

        # Move to the next match pair
        current = knockout_list.head


def user_command(groups, knockout_list, phase):
    """
    Handles user input for viewing rankings or continuing the simulation.

    Parameters:
        groups (list): The list of groups in the group stage.
        knockout_list (LinkedListt): The knockout stage linked list.
        phase (str): Either "group" or "knockout" to indicate the current phase.

    Returns:
        boolean: True to continue, False to stop.
    """
    while True:
        user_input = input("\nEnter 'S' to see standings, 'C' to continue: ").strip().upper()
        if user_input == "S":
            if phase == "group":
                display_group_rankings(groups)
            elif phase == "knockout":
                print("\nKnockout Stage Bracket:")
                current = knockout_list.head
                while current:
                    print(f"{current.get_data()['name']}")
                    current = current.get_next()
        elif user_input == "C":
            return True
        else:
            print("Invalid input. Please try again.")





def knockout_competition(teams, match_history):
    """
    Simulates the knockout competition from the Round of 16 to the Final.
    
    Parameters:
        teams (list): List of promoted teams (16 teams).
        match_history (MatchHistoryLinkedList): Linked list to store match history.

    Returns:
        dict: The champion team.
    """
    stages = ["Round of 16", "Quarterfinals", "Semifinals", "Final"]
    current_teams = teams
    game_number = match_history.size + 1

    for stage in stages:
        print(f"\n{stage} Matches:")
        next_round_teams = []

        for i in range(0, len(current_teams), 2):
            team1 = current_teams[i]
            team2 = current_teams[i + 1]

            # Simulate the knockout match
            winner, loser = knockout_match_play(team1, team2)
            print(f"{winner['name']} defeated {loser['name']}")
            
            # Add match result to history
            match_history.add_match(
                game_number, winner["name"], loser["name"], 0, 0
            )
            game_number += 1
            
            # Winner advances
            next_round_teams.append(winner)

        current_teams = next_round_teams

    # Final team is the champion
    champion = current_teams[0]
    return champion




def main():
    """
    Run the World Cup simulation.

    This function initializes teams and groups, runs group stage matches,
    promotes teams to the knockout stage, and determines the tournament winner.
    """
    # Load team data from the CSV file
    csv_file = 'teams.csv'
    all_teams, groups = initialize_teams(csv_file)

    if not all_teams or not groups:
        print("Error initializing teams. Exiting.")
        return

    # Initialize the Match History Linked List
    match_history = MatchHistoryLinkedList()

    # Display initial group rankings
    print("\nInitial Group Rankings:")
    display_group_rankings(groups)

    # Group stage simulation
    print("\nStarting Group Stage...")
    updated_groups = group_stage_matches(groups, match_history)

    # Handle user commands for group stage
    user_command = ""
    while user_command != "C":
        user_command = input("\nEnter 'S' to display rankings and match history, or 'C' to continue: ").strip().upper()
        if user_command == "S":
            print("\nGroup Rankings After Group Stage:")
            display_group_rankings(updated_groups)
            print("\nMatch History:")
            match_history.display_history()
        elif user_command != "C":
            print("Invalid command. Please enter 'S' or 'C'.")

    # Promote top teams to the knockout stage
    print("\nPromoting teams to the knockout stage...")
    knockout_list = setup_knockout_round(updated_groups)

    # Knockout stage simulation
    print("\nStarting Knockout Stage...")
    while knockout_list.size() > 1:
        print("\nKnockout Round Matches:")
        play_knockout_round(knockout_list, match_history)

        # Handle user commands for knockout stage
        user_command = ""
        while user_command != "C":
            user_command = input("\nEnter 'S' to display knockout results and match history, or 'C' to continue: ").strip().upper()
            if user_command == "S":
                print("\nKnockout Round Results:")
                knockout_list.display()
                print("\nMatch History:")
                match_history.display_history()
            elif user_command != "C":
                print("Invalid command. Please enter 'S' or 'C'.")

    # Determine the winner
    if knockout_list.head:
        winner = knockout_list.head.get_data()
        print(f"\nThe winner of the World Cup is: {winner['name']}!")

    print("\nFinal Match History:")
    match_history.display_history()

    print("\nThank you for playing the World Cup Simulation!")


if __name__ == "__main__":
    main()

