import random
from queuee import Queue
from stack import Stack

# Initialize deck and player structures
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
    items = [card.strip() for card in cd.readlines()]  # Remove whitespace/newlines
    random.shuffle(items)

# Check if the number of cards is correct
print(f"Total cards read from file: {len(items)}")
if len(items) < 44:
    raise Exception("Not enough cards in cards.txt. Ensure there are at least 44 cards.")

# Enqueue the cards in the deck queue
for item in items:
    deck.enqueue(item)

# Confirm deck size after enqueuing
print(f"Deck size after enqueuing: {deck.size()}")

# Enqueue the cards in each player's queue
for player in players_Queue:
    for _ in range(5):
        if not deck.is_Empty():
            card = deck.dequeue()
            print(f"Dequeued {card} for player queue")
            player.enqueue(card)
        else:
            raise Exception("Not enough cards in the deck for players' queues.")

# Push the cards into each player's stack
for player in players_Stack:
    for _ in range(5):
        if not deck.is_Empty():
            card = deck.dequeue()
            print(f"Dequeued {card} for player stack")
            player.push(card)
        else:
            raise Exception("Not enough cards in the deck for players' stacks.")

# Push 4 cards to the table stack
for _ in range(4):
    if not deck.is_Rmpty():
        card = deck.dequeue()
        print(f"Dequeued {card} for table")
        table.push(card)
    else:
        raise Exception("Not enough cards in the deck for the table.")

# Final check
print(f"Remaining cards in deck after setup: {deck.size()}")
