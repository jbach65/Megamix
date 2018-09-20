# Megamix

Algorithm Description:
    My algorithm for solving the megamix combines several of the techniques and tricks that we discussed in class. Using the knowledge that the solution and the initial randomization are both bidirectional, I started searching from both the solved state and attempting to find a way to the unsolved state and from the unsolved stats attempting to find a way to the solved state. That way if it found a way from the solved state to the unsolved state faster then that could be used in reverse to solve the megamix.

    I also kept a hashmap of the combinations visited starting from both the solved and unsolved states. that way, If when solving from the unsolved state, I hit a combination that has already been visited while exploring the solved state I can retrace my steps from the solved state to find a complete path; and vice versa.

Heuristic:
    My heuristic is this formula: sum(number of stickers out of place * the distance to the correct side)/15

    When "weighting" each node(or current combination) I use the number found by applying my heuristic, plus the current depth of the node in the tree.

    I decided after much testing to not convert to an integer when calculating the heuristic and instead just leave it as a float that way a the "closest" combination gets expanded first.

How to Run:
    Use "python3 megaMix.py <number of randomizations>" to run the program for a given number of randomizations. If no number is provided it will default to 8.

    The program begins by initializing a solved megamix. It then performs the provided number of random initial turns, and calls the solving function banana_split_v4() and when complete, prints the results in a form that can be easily read and checked if needed. Also once solved it prints out the number of nodes expanded and the depth at which the solution was found.

Data Types:
    I tried to make my data type as simple and small as possible. I decided to use strings to hold the current combination and numbers(plus a and b) to signify colors and sides. That meant that when I went to perform a twist I simply swapped indexes of the string, determined by hardcoded rules based on the megamix's structure. The only other data structures I used were dictionaries to hold the combinations already visited, with the key being the combination and the value being the path traversed to get there.

Data and Charts:
    I attached a data file containing the results from 60 sample runs. they consist of 5 runs per number of initial randomizations 1-12. I tracked the depth at which the optimal solution was found and the number of nodes expanded up to that point. I also took the average nodes expanded for each depth at which the solution was found. I tried to graph that but since the y axis grew exponentially I could not get a meaningful graph. However, the numbers clearly show the range in which a solution can be found.

What I Learned:
    I learned a lot about optimization, and through my many banana_split versions I learned how to search and evaluate better using the methods we discussed in class.

Limitations:
    I tested my program and it can find all solutions for mixes with up to 15 initial randomizations.  anything above 15 and it is not guaranteed to solve it. Sometimes it gets luck and gets it right, but worst case it does have a memory error. That is, after approximately 5 million nodes expanded.
