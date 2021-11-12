import decimal
from flask import Flask, render_template, request, redirect
import json
from uniswap import Uniswap
from web3 import Web3
import os

# Networks
networks = {
    "Ethereum Mainnet" : "https://mainnet.infura.io/v3/bf23d8eecbea43c38ab48f85c7d35056",
    "Ropsten Test Network" : "https://ropsten.infura.io/v3/bf23d8eecbea43c38ab48f85c7d35056"
    # ,"Kovan Test Network" : "https://kovan.infura.io/v3/bf23d8eecbea43c38ab48f85c7d35056",
    # "Rinkeby Test Network" : "https://rinkeby.infura.io/v3/bf23d8eecbea43c38ab48f85c7d35056",
    # "Görli Test Network" : "https://goerli.infura.io/v3/bf23d8eecbea43c38ab48f85c7d35056"
    }

# Token Addresses
tokens_main = {
    'ETH' : "0x0000000000000000000000000000000000000000",
    'BAT' : "0x0d8775f648430679a709e98d2b0cb6250d2887ef",
    'DAI' : "0x6B175474E89094C44Da98b954EedeAC495271d0F",
    'USDT' : "0xdac17f958d2ee523a2206206994597c13d831ec7",
    "UNI" : "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984",
    "BUSD" : "0x4fabb145d64652a948d72533023f6e7a623c7c53",
    "VEN" : "0xd850942ef8811f2a866692a623011bde52a462c1",
    "WBTC" : "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
    "WETH" : "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
}

# Token Addresses
tokens_ropsten = {
    'ETH' : "0x0000000000000000000000000000000000000000",
    'BAT' : "0xfc67a5421156b29ac073f62861c097b56225a4f8",
    'DAI' : "0xad6d458402f60fd3bd25163575031acdce07538d",
    'USDT' : "0x03f7cef050aac29954a97334c00920aa8919dc37",
    "UNI" : "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984",
    "BUSD" : "0x8cb744073b2c2074a109ddfd57f9b28ddb6f5f72",
    "VEN" : "0xe70f782a17fa535155b2461fd4001ca0eb4357f4",
    "WBTC" : "0x15bb34e906836fbbbb5bfaeb6122ac2168da408d",
}

def network_tokens(network):
    # allocates correct token addresses based on network
    if network == "Ethereum Mainnet":
        return tokens_main
    elif network == "Ropsten Test Network":
        return tokens_ropsten

# calculates price impact of trade
def calc_impact(token_in, token_out, amount_in, uniswap)-> float:
    amount_small = 10**2
    print(amount_small,token_in,token_out)
    cost_small = uniswap.get_price_input(token_in, token_out, amount_small)
    cost_amount = uniswap.get_price_input(token_in, token_out, amount_in)
    price_small = cost_small / amount_small
    price_amount = cost_amount / amount_in

    # prevents 0 divide error for USDT
    if price_small == 0:
        price_small = 10**-10
    print(price_small,price_amount)
    return (price_small - price_amount) / price_small


#calculates swap value and gas prices
def calculate(uniswap, original_tk, target_tk, original_amount):
    print(original_amount)
    # if original_tk == "0x0000000000000000000000000000000000000000":
    #     orig_decimal = 18
    # else:
    #     orig_decimal = uniswap.get_token(original_tk).decimals
    quantity, orig_decimal = coin_to_wei(uniswap,original_tk, original_amount)

    targ_decimal = uniswap.get_token(target_tk).decimals
    print(quantity)
    # quantity = float(original_amount) * 10 ** orig_decimal
    target_amount = uniswap.get_price_input(original_tk, target_tk, quantity)
    # price_impact = uniswap.estimate_price_impact(original_tk, target_tk, int(quantity))
    price_impact = calc_impact(original_tk,target_tk, quantity, uniswap)
    print(target_amount)
    print(price_impact)
    return(target_amount, price_impact, targ_decimal)

def coin_to_wei(uniswap, token, amount):
    if token == "0x0000000000000000000000000000000000000000":
        decimal = 18
    else:
        decimal = uniswap.get_token(token).decimals

    wei = float(amount) * 10 ** decimal
    return(int(wei), decimal)

# MAIN APPLICATION

app = Flask(__name__)
# commit testing
@app.route('/', methods=['GET', 'POST'])
def index():
    # page is loaded, need to simply display the form
    message = 'Click the calculate button to calculate target amount possible' #default message


    if request.method == 'GET':
        return render_template('index.html', title='Token Swap', message=message,tokens=tokens_main, networks=networks)
    elif request.method == 'POST':
        # form was submitted, need to get variables
        user_address = request.form['userAddress']
        priv_key = request.form['privKey']
        original_token = request.form['ogToken']
        original_amount = request.form['ogAmount']
        target_token = request.form['targetToken']

        # try:
        #     target_amount = request.form['targetAmount']
        # except KeyError:
        #     # form not submitted/calculate not pressed so no amount to display yet
        #     target_amount = ""
        network = request.form['network']
        
        if original_token == target_token:
            message = "Please ensure original and target tokens are different"
            return render_template('index.html', title='Token Swap', message=message,tokens=tokens_main, networks=networks,
             user_address=user_address, priv_key=priv_key, original_token=original_token, original_amount=original_amount)

        # Set up network
        # redirect with error message if fails
    # try:
        w3= Web3(Web3.HTTPProvider(networks[network]))
        if w3.isConnected():
            print(network, "successfully connected")
        else:
            message = "An error occured when connecting to " + network
            return render_template('index.html', title='Token Swap', message=message,tokens=tokens_main, networks=networks)
    # except:
        # message = "An error occured when connecting to " + network
        # return render_template('index.html', title='Token Swap', message=message,tokens=tokens, networks=networks)
        
        #Sets up Address
    # try:
        address = Web3.toChecksumAddress(user_address)
        if Web3.isChecksumAddress(address):
            uniswap = Uniswap(address=address, private_key=priv_key, version=3, provider=networks[network],web3=w3)
            print("success")
            
            tokens = network_tokens(network)

            orig_add = Web3.toChecksumAddress(tokens[request.form['ogToken']])
            targ_add = Web3.toChecksumAddress(tokens[request.form['targetToken']])
            print(tokens[request.form['ogToken']])
            print(orig_add)
            print(Web3.isChecksumAddress(orig_add))
            print(tokens[request.form['targetToken']])
            print(targ_add)
            print(Web3.isChecksumAddress(targ_add))
            print("Calculating: " + request.form['ogToken'] + "/" + request.form['targetToken'])
            target_amount, price_impact, targ_decimal = calculate(uniswap, orig_add, targ_add, original_amount)
           
            
            display = "Original Token: " + original_token + "\nOriginal Amount: " + original_amount + "\nTarget Token: "\
                    + target_token + "\nTarget Amount: " + str(target_amount/10**targ_decimal)
                
            return render_template('approve.html', title='Token Swap', 
                 form_params=display, message='Estimated Price Impact: ' + str(round(price_impact*100,2)) + '%', tokens=tokens, networks=networks, user_address=user_address,
                  priv_key=priv_key, original_token=original_token, original_amount=original_amount, target_amount=target_amount/10**targ_decimal, target_token=target_token, network=network)

                # return redirect("/approve")

        else:
            message = "Invalid Address"
            print("Address check failed")
            return render_template('index.html', title='Token Swap', message=message,tokens=tokens_main, networks=networks)
    # except:
        # message = "Invalid Address"
        # print("try failed")
        # return render_template('index.html', title='Token Swap', message=message,tokens=tokens, networks=networks)

      
        
        # need logic to make this dynamic, static for now
        # estimate_gas = 5
        # return render_template('index.html', title='Token Swap', form_params=display, message='Estimated gas price: ' + str(estimate_gas), tokens=tokens, networks=networks, user_address=user_address, priv_key=priv_key, original_token=original_token, original_amount=original_amount, target_amount=target_amount, target_token=target_token, network=network)


# @app.route('/approve', methods=['GET', 'POST'])
# def approve():
#     pass
    # if request.method == 'GET':
    #     return redirect("/")
    # else:
    #     # form was submitted, need to get variables
    #     user_address = request.form['userAddress']
    #     priv_key = request.form['privKey']
    #     original_token = request.form['ogToken']
    #     original_amount = request.form['ogAmount']
    #     target_token = request.form['targetToken']
    #     try:
    #         target_amount = request.form['targetAmount']
    #     except KeyError:
    #         # form not submitted/calculate not pressed so no amount to display yet
    #         target_amount = ""

    #     network = request.form['network']
    #     tokens = network_tokens(network)
    #     # Set up network
    #     # redirect with error message if fails
    #     try:
    #         w3= Web3(Web3.HTTPProvider(networks[network]))
    #         if w3.isConnected():
    #             print(networks[network], "successfully connected")
    #         else:
    #             message = "An error occured when connecting to " + networks[network]
    #             return render_template('index.html', title='Token Swap', message=message,tokens=tokens, networks=networks)
    #     except:
    #         message = "An error occured when connecting to " + networks[network]
    #         return render_template('index.html', title='Token Swap', message=message,tokens=tokens, networks=networks)
        

    #     #Sets up Address
    #     try:
    #         address = Web3.toChecksumAddress(user_address)
    #         if Web3.isChecksumAddress(address):
    #             # uniswap = Uniswap(address=address, private_key=priv_key, version=3, provider=w3) #w3 or w3_ropsten depending on testing or live
    #             print("Success")
    #         else:
    #             message = "Invalid Address"
    #             return render_template('index.html', title='Token Swap', message=message,tokens=tokens, networks=networks)
    #     except:
    #         message = "Invalid Address"
    #         return render_template('index.html', title='Token Swap', message=message,tokens=tokens, networks=networks)

    #     display = "Original Token: " + original_token + "   Original Amount: " + original_amount + "    Target Token: " + target_token + "  Target Amount: " + target_amount 
    #     # need logic to make this dynamic, static for now
    #     return render_template('approve.html', title='Token Swap', form_params=display, message='Estimated Price Impact: ' + str(round(price_impact*100,2)) + '%', tokens=tokens, networks=networks, user_address=user_address, priv_key=priv_key, original_token=original_token, original_amount=original_amount, target_amount=target_amount, target_token=target_token, network=network)

@app.route('/execute', methods=['GET', 'POST'])
def execute():
    if request.method == 'GET':
        return redirect("/")
    else:
        user_address = request.form['userAddress']
        priv_key = request.form['privKey']
        original_token = request.form['ogToken']
        original_amount = request.form['ogAmount']
        target_token = request.form['targetToken']
        target_amount = request.form['targetAmount']
        network = request.form['network']
        
        w3= Web3(Web3.HTTPProvider(networks[network]))
        address = Web3.toChecksumAddress(user_address)
        uniswap = Uniswap(address=address, private_key=priv_key, version=3, provider=networks[network],web3=w3)

        tokens = network_tokens(network)

        orig_add = Web3.toChecksumAddress(tokens[original_token])
        targ_add = Web3.toChecksumAddress(tokens[target_token])

        amount, orig_decimal = coin_to_wei(uniswap, orig_add, original_amount)

        uniswap.make_trade(orig_add,targ_add, amount)

        return render_template('confirmed.html', title='Confirmation', message='Your order has been placed')
        
        
        
