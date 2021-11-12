from flask import Flask, render_template, request, redirect
import json
from uniswap import Uniswap
from web3 import Web3
import os

# Networks
networks = {
    "Ethereum Mainnet" : "https://mainnet.infura.io/v3/bf23d8eecbea43c38ab48f85c7d35056",
    "Ropsten Test Network" : "https://ropsten.infura.io/v3/bf23d8eecbea43c38ab48f85c7d35056",
    "Kovan Test Network" : "https://kovan.infura.io/v3/bf23d8eecbea43c38ab48f85c7d35056",
    "Rinkeby Test Network" : "https://rinkeby.infura.io/v3/bf23d8eecbea43c38ab48f85c7d35056",
    "Görli Test Network" : "https://goerli.infura.io/v3/bf23d8eecbea43c38ab48f85c7d35056"
    }

# Token Addresses
tokens = {
    'ETH' : "0x0000000000000000000000000000000000000000",
    'BAT' : "0x0D8775F648430679A709E98d2b0Cb6250d2887EF",
    'DAI' : "0x6B175474E89094C44Da98b954EedeAC495271d0F",
    'WETH' : "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
}

#calculates swap value and gas prices
def calculate(uniswap, original_tk, target_tk, original_amount, w3):
    print(original_amount)
    target_amount = uniswap.get_price_input(original_tk, target_tk, int(original_amount))
    gas_price = Web3.fromWei(w3.eth.gas_price,'ether')
    print(target_amount)
    print(gas_price)
    return(target_amount, gas_price)

app = Flask(__name__)
# commit testing
@app.route('/', methods=['GET', 'POST'])
def index():
    # page is loaded, need to simply display the form
    message = 'Click the calculate button to calculate target amount possible' #default message


    if request.method == 'GET':
        return render_template('index.html', title='Token Swap', message=message,tokens=tokens, networks=networks)
    elif request.method == 'POST':
        # form was submitted, need to get variables
        user_address = request.form['userAddress']
        priv_key = request.form['privKey']
        original_token = request.form['ogToken']
        original_amount = request.form['ogAmount']
        target_token = request.form['targetToken']
        try:
            target_amount = request.form['targetAmount']
        except KeyError:
            # form not submitted/calculate not pressed so no amount to display yet
            target_amount = ""
        network = request.form['network']
        

        # Set up network
        # redirect with error message if fails
        try:
            w3= Web3(Web3.HTTPProvider(networks[network]))
            if w3.isConnected():
                print(network, "successfully connected")
            else:
                message = "An error occured when connecting to " + network
                return render_template('index.html', title='Token Swap', message=message,tokens=tokens, networks=networks)
        except:
            message = "An error occured when connecting to " + network
            return render_template('index.html', title='Token Swap', message=message,tokens=tokens, networks=networks)
        

        # # CODE FOR GENERATING ALL TOKENS
        # # uniswap_Factory
        # factory_abi = json.loads('[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
        # factory_address = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
        # factory_contract = w3.eth.contract(address=factory_address, abi=factory_abi)
        # allPairsLength = factory_contract.functions.allPairsLength().call()
        # print('number of pairs in factory:' , allPairsLength)

        # for i in range(1, allPairsLength):
        #     allPairs_address = factory_contract.functions.allPairs(i).call()
        #     contract = w3.eth.contract(address=allPairs_address, abi=pairs_abi)
        #     symbol = contract.functions.name().call()
        #     supply = contract.functions.totalSupply().call()
        #     print(allPairs_address, supply)



        #Sets up Address
    # try:
        address = Web3.toChecksumAddress(user_address)
        if Web3.isChecksumAddress(address):
            uniswap = Uniswap(address=user_address, private_key=priv_key, version=3, provider=networks[network])
            print("success")
            
            if 'calculate' in request.form:
                target_amount, gas_price = calculate(uniswap, original_token, target_token, original_amount,w3)

            orig_add = Web3.toChecksumAddress(tokens[request.form['ogToken']])
            targ_add = Web3.toChecksumAddress(tokens[request.form['targetToken']])

            print("Calculating: " + request.form['ogToken'] + "/" + request.form['targetToken'])
            target_amount, gas_price = calculate(uniswap, orig_add, targ_add, original_amount,w3)
            # target_amount, gas_price = calculate(uniswap, request.form['ogToken'].lower(), request.form['targetToken'].lower(), original_amount,w3)

        else:
            message = "Invalid Address"
            print("if failed")
            return render_template('index.html', title='Token Swap', message=message,tokens=tokens, networks=networks)
    # except:
        # message = "Invalid Address"
        # print("try failed")
        # return render_template('index.html', title='Token Swap', message=message,tokens=tokens, networks=networks)

        display = "Original Token: " + original_token + "\nOriginal Amount: " + original_amount + "\nTarget Token: " + target_token + "\nTarget Amount: " + str(target_amount)
        # need logic to make this dynamic, static for now
        estimate_gas = 5
        return render_template('index.html', title='Token Swap', form_params=display, message='Estimated gas price: ' + str(estimate_gas), tokens=tokens, networks=networks, user_address=user_address, priv_key=priv_key, original_token=original_token, original_amount=original_amount, target_amount=target_amount, target_token=target_token, network=network)


@app.route('/approve', methods=['GET', 'POST'])
def approve():
    if request.method == 'GET':
        return redirect("/")
    else:
        # form was submitted, need to get variables
        user_address = request.form['userAddress']
        priv_key = request.form['privKey']
        original_token = request.form['ogToken']
        original_amount = request.form['ogAmount']
        target_token = request.form['targetToken']
        try:
            target_amount = request.form['targetAmount']
        except KeyError:
            # form not submitted/calculate not pressed so no amount to display yet
            target_amount = ""
        network = request.form['network']

        # Set up network
        # redirect with error message if fails
        try:
            w3= Web3(Web3.HTTPProvider(networks[network]))
            if w3.isConnected():
                print(networks[network], "successfully connected")
            else:
                message = "An error occured when connecting to " + networks[network]
                return render_template('index.html', title='Token Swap', message=message,tokens=tokens, networks=networks)
        except:
            message = "An error occured when connecting to " + networks[network]
            return render_template('index.html', title='Token Swap', message=message,tokens=tokens, networks=networks)
        

        #Sets up Address
        try:
            address = Web3.toChecksumAddress(user_address)
            if Web3.isChecksumAddress(address):
                # uniswap = Uniswap(address=address, private_key=priv_key, version=3, provider=w3) #w3 or w3_ropsten depending on testing or live
                print("Success")
            else:
                message = "Invalid Address"
                return render_template('index.html', title='Token Swap', message=message,tokens=tokens, networks=networks)
        except:
            message = "Invalid Address"
            return render_template('index.html', title='Token Swap', message=message,tokens=tokens, networks=networks)

        display = "Original Token: " + original_token + "   Original Amount: " + original_amount + "    Target Token: " + target_token + "  Target Amount: " + target_amount 
        # need logic to make this dynamic, static for now
        estimate_gas = 5
        return render_template('approve.html', title='Token Swap', form_params=display, message='Estimated gas price: ' + str(estimate_gas), tokens=tokens, networks=networks, user_address=user_address, priv_key=priv_key, original_token=original_token, original_amount=original_amount, target_amount=target_amount, target_token=target_token, network=network)

@app.route('/execute', methods=['GET', 'POST'])
def execute():
    if request.method == 'GET':
        return redirect("/")
    else:
        # form was submitted, need to get variables
        user_address = request.form['userAddress']
        priv_key = request.form['privKey']
        original_token = request.form['ogToken']
        original_amount = request.form['ogAmount']
        target_token = request.form['targetToken']
        try:
            target_amount = request.form['targetAmount']
        except KeyError:
            # form not submitted/calculate not pressed so no amount to display yet
            target_amount = ""
        network = request.form['network']

        # Set up network
        # redirect with error message if fails
        try:
            w3= Web3(Web3.HTTPProvider(networks[network]))
            if w3.isConnected():
                print(networks[network], "successfully connected")
            else:
                message = "An error occured when connecting to " + networks[network]
                return render_template('index.html', title='Token Swap', message=message,tokens=tokens, networks=networks)
        except:
            message = "An error occured when connecting to " + networks[network]
            return render_template('index.html', title='Token Swap', message=message,tokens=tokens, networks=networks)
        

        #Sets up Address
        try:
            address = Web3.toChecksumAddress(user_address)
            if Web3.isChecksumAddress(address):
                # uniswap = Uniswap(address=address, private_key=priv_key, version=3, provider=w3) #w3 or w3_ropsten depending on testing or live
                print("Success")
            else:
                message = "Invalid Address"
                return render_template('index.html', title='Token Swap', message=message,tokens=tokens, networks=networks)
        except:
            message = "Invalid Address"
            return render_template('index.html', title='Token Swap', message=message,tokens=tokens, networks=networks)

        display = "Original Token: " + original_token + "   Original Amount: " + original_amount + "    Target Token: " + target_token + "  Target Amount: " + target_amount 
        # need logic to make this dynamic, static for now
        estimate_gas = 5
        return render_template('execute.html', title='Token Swap', form_params=display, message='Estimated gas price: ' + str(estimate_gas), tokens=tokens, networks=networks, user_address=user_address, priv_key=priv_key, original_token=original_token, original_amount=original_amount, target_amount=target_amount, target_token=target_token, network=network)