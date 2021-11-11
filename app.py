from flask import Flask, render_template, request
from uniswap import Uniswap
from web3 import Web3
import os

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/bf23d8eecbea43c38ab48f85c7d35056'))
print("Main Net Connected:", w3.isConnected()) 

w3_ropsten = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/bf23d8eecbea43c38ab48f85c7d35056')) # used for testing on ropsten network
print("Ropsten Net Connected:", w3_ropsten.IsConnected())

# Token Addresses
tokens = {
    'ETH' : "0x0000000000000000000000000000000000000000",
    'BAT' : "0x0D8775F648430679A709E98d2b0Cb6250d2887EF",
    'DAI' : "0x6B175474E89094C44Da98b954EedeAC495271d0F",
    'WETH' : "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
}



app = Flask(__name__)
# commit testing
@app.route('/', methods=['GET', 'POST'])
def index():
    # page is loaded, need to simply display the form
    if request.method == 'GET':
        return render_template('index.html', title='Token Swap', message='Click the Submit button to Swap your tokens',tokens=tokens)
    elif request.method == 'POST':
        # form was submitted, need to get variables
        user_address = request.form['userAddress']
        priv_key = request.form['privKey']

        original_token = request.form['ogToken']
        original_amount = request.form['ogAmount']
        target_token = request.form['targetToken']
        target_amount = request.form['targetAmount']

        #Checks if valid address
        try:
            address = Web3.toChecksumAddress(user_address)
            if Web3.isChecksumAddress(address):
                uniswap = Uniswap(address=address, private_key=priv_key, version=3, provider=w3_ropsten) #w3 or w3_ropsten depending on testing or live

            else:
                add_check = "Invalid Address"
        except:
            add_check = "Invalid Address"

        display = "Original Token: " + original_token + "\nOriginal Amount: " + original_amount + "\nTarget Token: " + target_token + "\nTarget Amount: " + target_amount 
        # need logic to make this dynamic, static for now
        estimate_gas = 5
        return render_template('index.html', title='Token Swap', form_params=display, message='Estimated gas price: ' + str(estimate_gas), tokens=tokens)

    