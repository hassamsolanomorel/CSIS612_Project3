# CSIS612_Project3

### Required Dependencies
- Python 3.7
- terminaltables (python library)

### How to run it!!
1. Clone this repo to your local machine
2. Ensure you have python 3.7 or above by running `python3 --version`
3. Download the terminaltables library by running `pip3 install terminaltables`
4. `cd` to the root folder of the repo you just cloned
5. Run `python3 main.py` to start the application
6. Follow the on screen instructions. (Have Fun!!)

### Sample Instructions
Try these combinations (remember these instructions are entered one at a time in the program):
#### Combo1 (Test Write-After-Reads)
add R1 R2 R3

add R2 R3 R4
#### Combo2 (Test Write-After-Write)
add R1 R2 R3

add R1 R3 R4
#### Combo3 (Test Write-After-Read with a True Dependence)
add R1 R2 R3

add R2 R1 R4

add R1 R5 R6
#### Combo4 (Test Write-After-Write with a True Dependence)
add R1 R2 R3

add R1 R1 R4
#### Combo3 (Just having Fun)
add R1 R2 R3

add R1 R1 R3

add R1 R2 R3

add R3 R1 R2

add R4 R2 R1
