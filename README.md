# Oskour

## Presentation

The goal of this project is to solve the following problem:

Given:
1. $N$ gamemaster (gm), let us define $A_{i,j,k}$ : the gm $i$ is available at round $j$ for the rpg $k$
2. $K$ rounds
3. $M$ teams, let us define $s_{i,j}$ the size of the team $i$ at round $j$
4. $S$ rpgs requiring $M_i$ players maximum and $m_i$ players minimum

Assign teams to each gamemaster at each round with an rpgs which maximizes the satisfaction of each team and respects the size, availability and custom constrains.


## Usage

As a package, the solver can be launched as ```python -m oskour [input_directory] [output_directory]```


## Installation

Dependencies are : ```Panda NumPy  PuLP```




