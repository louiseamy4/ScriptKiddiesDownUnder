from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # page is loaded, need to simply display the form
    if request.method == 'GET':
        return render_template('index.html', title='Token Swap')
    elif request.method == 'POST':
        # form was submitted, need to get variables
        original_token = request.form['ogToken']
        original_amount = request.form['ogAmount']
        target_token = request.form['targetToken']
        target_amount = request.form['targetAmount']
        display = "Original Token: " + original_token + "\nOriginal Amount: " + original_amount + "\nTarget Token: " + target_token + "\nTarget Amount: " + target_amount 
        return render_template('index.html', title='Token Swap', form_params=display)