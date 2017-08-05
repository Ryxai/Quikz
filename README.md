# Quikz
Python script to implement a quiz maker/taker/grader.
Designed to run over the command line. Designed for quiz taking as a part of self-study.
Due to the design of python, functionality inherently more advanced then multiple/choice or 'range-limited' inputs
is not possible at the current time. [Failures of python sandboxing](https://lwn.net/Articles/574215/) is abailable
on why making quizzes that can evaluate python scripts directly would be easily exploitable. 

##API
The script is importable
```
from Quikz import Quiz
```
Which can then be used by a more complicated application.

##Running the script directly
Can be run directly to make, take or modify existing quizzes. Can read and write quizzes to JSON 
files on disk. A bash script could be used to automate test taking across a group of individuals. 
