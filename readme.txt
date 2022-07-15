USAGE:
python3 main.py <{'|'.join(cmds)}>
max = guess fraudulent if the heuristic for the best column finds it
and = guess fraudulent if ALL the heuristics determined to be good find it

the goodness of a heuristic is determined by the proportion of rows it can correctly determine the class of

i.e. if the accuracy is .90, guess = Class 90% of the time