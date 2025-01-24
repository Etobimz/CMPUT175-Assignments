import random
from queuee import Queue
from stack import Stack

# Create the deck queue and the players' stacks, queues, and table
deck = Queue(52)
player_queue1 = Queue(5)
player_stack1 = Stack(5)
player_queue2 = Queue(5)
player_stack2 = Stack(5)
player_queue3 = Queue(5)
player_stack3 = Stack(5)
player_queue4 = Queue(5)
player_stack4 = Stack(5)
table = Stack(4)

# Store players' stacks and queues
players_Queue = [player_queue1, player_queue2, player_queue3, player_queue4]
players_Stack = [player_stack1, player_stack2, player_stack3, player_stack4]

# Read the cards from a text file and fill up the deck queue
with open('cards.txt', 'r') as cd:
    items = [card.strip() for card in cd.readlines()]
    random.shuffle(items)  # Shuffle the deck

# Enqueue the cards in the deck queue
for item in items:
    deck.enqueue(item)

# Enqueue the cards in each player's queue
for player in players_Queue:
    for _ in range(5):
        card = deck.dequeue()
        player.enqueue(card)

# Push the cards into each player's stack
for player in players_Stack:
    for _ in range(4):
        card = deck.dequeue()
        player.push(card)

# Push 4 cards to the table stack
for _ in range(4):
    card = deck.dequeue()
    table.push(card)

# Color code dictionary
color_code_dict = {'R': '\033[41m', 'G': '\033[42m', 'O': '\033[43m', 'P': '\033[105m'}
reset_code = '\033[0m'

def colorize_card(card):
    """
    Adds color to a card string based on its color identifier.
    """
    color_code = color_code_dict.get(card[1], '')
    return f"{color_code}{card}{reset_code}"

def display_table(table_stack):
    """
    Displays the current cards on the table with colors and restores them to the table stack.
    """
    print("Table:", end=' ')
    temp_table = []
    while not table_stack.isEmpty():
        card = table_stack.pop()
        temp_table.append(card)
        print(colorize_card(card), end=' ')
    print()
    
    for card in reversed(temp_table):
        table_stack.push(card)

def display_game_state(players_Queue, players_Stack, table_stack):
    """
    Displays the current game state, including each player's queue, stack, and the table stack.
    """
    print("Current Game State:\n")
    for player_num in range(4):
        print(f"Player {player_num + 1}:")
        
        # Display Queue
        print("Queue -> ", end="")
        temp_queue = []
        while not players_Queue[player_num].isEmpty():
            card = players_Queue[player_num].dequeue()
            temp_queue.append(card)
            print(f"| {colorize_card(card)} ", end="")
        print("|")
        
        # Restore queue
        for card in temp_queue:
            players_Queue[player_num].enqueue(card)
        
        # Display Stack
        print("         Stack -> ", end="")
        temp_stack = []
        while not players_Stack[player_num].isEmpty():
            card = players_Stack[player_num].pop()
            temp_stack.append(card)
            print(f"[ {colorize_card(card)} ] ", end="")
        print()

        # Restore stack
        for card in reversed(temp_stack):
            players_Stack[player_num].push(card)
        
        print("\n" + "-" * 30)
    
    # Display Table
    print("The Table:")
    display_table(table_stack)
    print("\n" + "=" * 50)

def find_match(player_stack, table_stack):
    """
    Checks if a player's top card and any table card sums to 15.
    """
    if player_stack.isEmpty():
        return None, None
    
    player_card = player_stack.pop()
    player_val = int(player_card[0])
    
    temp_table = []
    match_card = None
    for _ in range(4):
        if table_stack.isEmpty():
            break
        table_card = table_stack.pop()
        temp_table.append(table_card)
        table_val = int(table_card[0])
        
        if player_val + table_val == 15:
            match_card = table_card
            break

    for card in reversed(temp_table):
        if card != match_card:
            table_stack.push(card)

    if match_card:
        return player_card, match_card
    else:
        player_stack.push(player_card)
        return None, None

def play_turn(player_stack, player_queue, player_num, table_stack, deck_queue, player_scores, round_num):
    """
    Executes a player's turn, handling matching, discarding, or changing.
    """
    print(f"Round: {round_num + 1}, Player {player_num + 1} is playing.")

    if player_stack.isEmpty():
        print(f"Player {player_num + 1} has no more cards in their stack.")
        return

    match_card, table_card = find_match(player_stack, table_stack)
    if match_card:
        print(f"Player {player_num + 1} gets 15 points by matching {colorize_card(match_card)} from hand and {colorize_card(table_card)} from the table.")
        player_scores[player_num] += 15
        deck_queue.enqueue(match_card)
        deck_queue.enqueue(table_card)
        table_stack.push(deck_queue.dequeue())
    else:
        print(f"No Matches for Player {player_num + 1}, would you like to Discard(D/d) the card or swap (S/s)?")
        choice = input().lower()
        if choice == 'd':
            print(f"Player {player_num + 1} discarded the card on hand!")
            deck_queue.enqueue(player_stack.pop())
        elif choice == 's':
            if not player_queue.isEmpty():
                print(f"Player {player_num + 1} swaps the card {colorize_card(player_queue.dequeue())} from the queue.")
                player_queue.enqueue(player_stack.pop())
            else:
                print("No more cards to swap in queue.")
        else:
            print("Invalid choice!")
            deck_queue.enqueue(player_stack.pop())
        
        display_table(table_stack)

def determine_winner(player_scores):
    """
    Determines the winner by highest score and saves results to the requred game_score txtx  file.
    """
    max_score = max(player_scores)
    winners = [i + 1 for i, score in enumerate(player_scores) if score == max_score]

    with open("game_score.txt", "w") as f:
        f.write("Scores:\n")
        for i, score in enumerate(player_scores):
            f.write(f"Player_{i + 1} = {score:.1f};\n")

        if len(winners) == 1:
            f.write(f"Player {winners[0]} wins!\n")
        elif len(winners) == 4:
            f.write("It's a tie! No one Wins!\n")
        else:
            winners_str = " and ".join(f"Player {w}" for w in winners)
            f.write(f"{winners_str} win!\n")

# Gameplay
player_scores = [0, 0, 0, 0]

# Display initial game state
display_game_state(players_Queue, players_Stack, table)

# Each player completes all 5 rounds before moving to the next player
for player_num in range(4):
    for round_num in range(5):
        play_turn(players_Stack[player_num], players_Queue[player_num], player_num, table, deck, player_scores, round_num)
        display_game_state(players_Queue, players_Stack, table)  # Display game state after each turn

# Determine and write winner information
determine_winner(player_scores)
