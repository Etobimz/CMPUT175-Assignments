class Stack:
    def __init__(self, capacity):
        self.items = []
        self.__capacity = capacity
    
    def push(self, item):
        self.items.append(item)
    
    
    def pop(self):
        """
        Function to pop the last item in a stack and raises an IndexError if the stack is empty
        Parameters: None
        """
        if not self.items: # Check if the stack is empty
            raise IndexError("You are trying to pop an item from an empty stack ")
        else:
            return self.items.pop() # pop the last item in a stack
    
    def peek(self):      
        """
        Function to peep the last item in a stack and raises an IndexError if the stack is empty
        Parameters: None

        """
        if not self.items: # Check if the stack is empty
            raise IndexError("You are trying to peep an item in an empty stack ")
        else:
            return self.items[len(self.items)-1]  # View the top item without removing it

    
    def isEmpty(self):
        return self.items == []
    
    def size(self):
        return len(self.items)
    
    def show(self):
        print(self.items)
    
    def __str__(self):
        stackAsString = ''
        for item in self.items:
            stackAsString += item + ' '
        return stackAsString
    
    def clear(self):
        """
        The Function Removes all items currently in a stack and does nothing if the stack is currently empty.
        Parameters: None
        """
        self.items = [] # Replaces/Overwrites the current stack with a new empty stack clearing the former stack be it empty or contained.


