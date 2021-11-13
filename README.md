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
- Will need wallet address and private key 
- These values are entered into the swap form 
- Also selected is the original token and the target token
- An amount of the original token is entered
- On submitting this initial form via calculate, the program will
calculate the equivalent amount of target token and display a price impact
- Based on these figures, the user can then execute the swap, or navigate to the 
main page to adjust values 

=========== Issues to be resolved ============
Price impact estimation is inaccurate, it is on the roadmap to resolve this.

Application will crash if transaction amount exceeds token balance, it is on the roadmap to resolve this.

A number of pairs produce "web3.exceptions.ContractLogicError: execution reverted" errors when attempting to get the price conversion from original to target token. There are currently 30 working pairs.
The following pairs are functional:

Ethereum Mainnet
o	ETH to BAT
o	ETH to DAI
o	ETH to UNI
o	ETH to USDT
o	ETH to BUSD
o	ETH to WBTC
o	DAI to BAT
o	DAI to UNI
o	DAI to WTBC
o	DAI to WETH
o	USDT to DAI
o	USDT to UNI
o	USDT to WBTC
o	USDT to WETH
o	BAT to DAI
o	UNI to DAI
o	UNI to USDT
o	UNI to WBTC
o	UNI to WETH
o	BUSD to WETH
o	WBTC to DAI
o	WBTC to USDT
o	WTBC to UNI
o	WTBC to WETH
o	WETH to BAT
o	WETH to DAI
o	WETH to USDT
o	WETH to UNI
o	WETH to BUSD
o	WETH to WBTC

Ropsten Test Newtork
o	ETH to DAI
o	ETH to UNI


Note that Currently the user cannot convert to ETH to WETH or any other Token to ETH on Mainnet, it is in the roadmap to resolve this.