# ScriptKiddiesDownUnder

A python Flask application that hosts our DEX platform. 

Requirements: Python 3.9 

To run program:
Create a virtual env and install dependencies from requirements.txt via:
- Place the requirements.txt in desired directory
- Navigate to the directory via command line
- pip install -r requirements.txt

Once dependencies have been installed, ensure in main directory (with app.py) and run 
flask run 
command in the command line to host the app on user's local host.

To interact with app:
- Will need metamask wallet address and private key 
- These values are entered into the swap form 
- Also selected is the original token and the target token
- An amount of the original token is entered
- On submitting this initial form via calculate, the program will
calculate the equivalent amount of target token and display a price impact
- Based on these figures, the user can then execute the swap, or navigate to the 
main page to adjust values 
