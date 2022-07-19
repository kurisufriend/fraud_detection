USAGE:
<<<<<<< HEAD
python3 main.py

uses sklearn's SGD classifier
=======
python3 main.py <max|and>
max = guess fraudulent if the heuristic for the best column finds it
and = guess fraudulent if ALL the heuristics determined to be good find it

the goodness of a heuristic is determined by the proportion of rows it can correctly determine the class of

i.e. if the accuracy is .90, guess = Class 90% of the time
>>>>>>> a05b791646edb8095704fc22880ddf7b95a9b241
