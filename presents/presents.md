Considering the original design for their present algorithm. A number of things could have gone wrong.
Two servants could have been attempting to remove the same present which could have resulted in a double delete depending on how their remove_present function was written. It was likely they mismanaged their multiprocessing lock.

For my implementation I imagined a quite simple solution while holding the three intended functions constant: 
    - 1 -
    Add a present from the bag in order of that servant's range
    - 2 -
    Remove a present from the linked list randomly
    - 3 -
    Have a 1% chance per loop to search for a random tag

Additionally I used implementations for Nodes and Linked Lists in accordance to standard linked list practices.

For the runtime it started with 13s, and for each consecutive run it got shorter, my last runtime was 0.73s

To make the code better or more realistic I can make it a random chance to do any of the 3 actions instead of how it is currently--do action 1, do action 2, maybe do 3 then loop.

to run from within the presents folder do 
```
python3 presents.py
```
to run from within the parent folder do 
```
python3 presents/presents.py
```