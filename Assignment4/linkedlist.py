import random
                
class LinkedListNode:
    """
    # an instance of this class is a node in a Single Linked List

    Parameters:
            data (dict): A dictionary containing team information.
            Includes "Team name", "power", "points", "wins", "losses", "draws", and "GD".
    """

    def __init__(self, data):
        """
        Initializes a node with the provided data.

        Parameters:
            data (dict): A dictionary containing team information (name, power, points, GD.)


        Returns:
            None
        """

        self.data = data
        self.next_node = None

    def get_data(self):
        """
        Returns the team data stored in the node.

        Returns:
            dict: The team data.
        """
        return self.data
    

    def set_data(self, data):
        """
        Updates the team data stored in the node.

        Parameters:
            data (dict): The updated team data.
        """
        self.data = data

    def get_next(self):
        """
        Returns the next node in the list.

        Returns:
            LinkedListNode: The next node, or None if this is the last node.
        """
        return self.next_node

    def set_next(self, new_next):
        """
        Sets the next node in the list.

        Parameters:
            new_next (LinkedListNode): The node to set as the next node.
        """
        self.next_node = new_next



class LinkedListt:
    """
    Class representing a linked list of teams and their points.

    Attributes:
        head (LinkedListNode): The head node of the linked list.
    """

    def __init__(self):
        """
        Initializes an empty linked list.

        Returns:
            None
        """
        self.head = None

    

    def append_team(self, team):
        """
        Append a team as a node to the linked list.
    
        Parameters:
        team (dict): A dictionary containing team data.
        """
        new_node = LinkedListNode(team)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.get_next():
                current = current.get_next()
            current.set_next(new_node)

    def delete(self, team_name):
        """
        Remove a team from the linked list by its name.
    
        Parameters:
        team_name (str): The name of the team to remove.
        """
        if not self.head:
            print("The list is empty.")
            return

        # If the team is at the head
        if self.head.get_data()["name"] == team_name:
            self.head = self.head.get_next()
            return

        # Traverse to find and delete the team
        current = self.head
        previous = None
        while current and current.get_data()["name"] != team_name:
            previous = current
            current = current.get_next()

        if not current:
            print(f"Team '{team_name}' not found.")
            return

        # Remove the team
        previous.set_next(current.get_next())




    def sort(self, key=None, reverse=False):
        """
        Sorts the linked list in-place based on the provided key function.

        Parameters:
            key (function, optional): A function that takes a team data dictionary
                                      and returns a value to sort by. If None, sorts by the
                                      dictionary itself. Defaults to None.
            reverse (bool, optional): Whether to sort in descending order. Defaults to False.
        """
        if not self.head or not self.head.next_node:
            return # Nothing to sort if list is empty or has only one element

        nodes = []
        current = self.head
        while current:
            nodes.append(current)
            current = current.get_next()

        self.head = None # Temporarily detach the list for sorting

        # Sort the nodes list based on the key function:
        nodes.sort(key=lambda node: key(node.data) if key else node.data, reverse=reverse)

        # Reconstruct the linked list from the sorted nodes:
        self.head = nodes[0]
        current = self.head
        for i in range(1, len(nodes)):
            current.set_next(nodes[i])
            current = current.get_next()
        current.set_next(None) # Ensure the tail's next is None



    def update_team_points(self, team_name, new_points):
            """
            Updates the points of a team in the linked list.

            Parameters:
            team_name (str): The name of the team to update.
            new_points (int): The new points to assign to the team.
            """

            current = self.head
            while current:
                team_data = current.get_data()
                if team_data["name"] == team_name: # Access "name" from the dictionary
                    team_data["points"] = new_points # Update "points" within the dictionary
                    current.set_data(team_data) # Very important, update the node's data
                    return
                current = current.get_next()

            print(f"Team '{team_name}' not found in the list.") # Or raise exception


    def display_rankings(self): # Now a method of LinkedListt to display its own rankings
            """Displays team rankings within the current linked list."""
            print("-------------------------------------------------------")
            print("| Team         | Points | Wins | Draws | Losses | GD |")
            print("-------------------------------------------------------")

            current = self.head
            while current:
                team_data = current.get_data()
                print(f"| {team_data['name']:<12} | {team_data['points']:>6} | {team_data['wins']:>4} | {team_data['draws']:>5} | {team_data['losses']:>6} | {team_data['GD']:>3} |")
                current = current.get_next()
          
            print("-------------------------------------------------------")


    def extract_teams_from_group(group): 
        """Extracts teams from the current linked list and returns a list of team data dictionaries."""
        teams = []
        current = group.head

        if not current:
            print("Warning: Group is empty (head is None).")
            return teams # Return empty list if group is empty
        
        while current:
            team_data = current.get_data()
            if team_data is None:
                print("Error: Found a node with no data.")
                return [] # Return empty list if node data is missing
            teams.append(team_data.copy()) # Append copies to prevent modification of original data

            current = current.get_next()

        return teams

    def display_group_rankings(groups): 
        """Displays rankings for all groups."""
        for i, group in enumerate(groups):
            group_name = chr(ord('A') + i) # Get group name (A, B, C, etc.)
            print(f"\nRankings for Group {group_name}:")
            group.display_rankings() # Call display_rankings on each group (LinkedListt)

    

    def __len__(self):
        """
        Returns the number of nodes (teams) in the linked list.
        """
        count = 0
        current = self.head
        while current is not None:
            count += 1
            current = current.getNext()
        return count



    def size(self):
        """
        Retrieve the number of nodes in the linked list.

        Returns:
            int: The number of nodes in the linked list.
        """
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.get_next()
        return count



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


    



class MatchHistoryNode:
    """Node class to represent a match in the match history linked list."""
    def __init__(self, game_number, team1, team2, team1_goals, team2_goals):
        self.data = {
            "game_number": game_number,
            "team1": team1,
            "team2": team2,
            "team1_goals": team1_goals,
            "team2_goals": team2_goals
        }
        self.next = None

    def get_data(self):
        return self.data

    def set_next(self, next_node):
        self.next = next_node

    def get_next(self):
        return self.next
    


class MatchHistoryLinkedList:
    """Linked list to track the history of matches."""
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def add_match(self, game_number, team1, team2, team1_goals, team2_goals):
        """Add a new match to the history."""
        new_node = MatchHistoryNode(game_number, team1, team2, team1_goals, team2_goals)
        if not self.head:
            self.head = new_node
        else:
            self.tail.set_next(new_node)
        self.tail = new_node
        self.size += 1

    def display_history(self):
        """Prints all matches in the history."""
        current = self.head
        while current:
            match = current.get_data()
            print(f"Game {match['game_number']}: {match['team1']} {match['team1_goals']} - {match['team2_goals']} {match['team2']}")
            current = current.get_next()
