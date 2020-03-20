# Import libraries
from flask import Flask, jsonify, request, render_template, make_response, session
from noobchain.Node import Node
from argparse import ArgumentParser
from threading import Thread
import time
import psutil

app = Flask(__name__, static_folder='static')
app.secret_key = 'sec_key'

#HOST = '127.0.0.1'
#PORT = 4000

# .......................................................................................
### REST API ###


# Home page
@app.route('/')
def home():
    # Store host ip and port
    session['HOST'] = HOST
    session['PORT'] = PORT
    # Keep track of current page
    session['viewing'] = 'home'
    # pass data to page call
    data = {
        'CPU_PERCENT': psutil.cpu_percent(),
        'MEM_PERCENT': psutil.virtual_memory()[2]
    }
    return render_template('home.html', data=data)


# Help
@app.route('/help', methods=['GET'])
def help():
    session['viewing'] = 'help'
    return render_template('help.html')


# About
@app.route('/about', methods=['GET'])
def about():
    session['viewing'] = 'about'
    return render_template("about.html")


# Contact
@app.route('/contact', methods=['GET'])
def contact():
    session['viewing'] = 'contact'
    return render_template("contact.html")


# Frequently Asked Questions
@app.route('/faq', methods=['GET'])
def faq():
    session['viewing'] = 'faq'
    return render_template("faq.html")


# User's Profile
@app.route('/profile', methods=['GET'])
def profile():
    session['viewing'] = 'profile'
    return render_template("profile.html")


# View last transactions in the blockchain
@app.route('/transactions/view', methods=['GET'])
def get_transactions():
    # transactions = Blockchain.transactions
    response = 0  # {'transactions': transactions}
    return render_template("view_last_transactions.html")


# Show balance
@app.route('/show_balance', methods=['GET'])
def show_balance():
    # transactions = blockchain.transactions
    response = 0  # {'transactions': transactions}
    return render_template("show_balance.html")


# Create a transaction
@app.route('/transactions/create', methods=['POST'])
def create_transaction():
    message = request.get_json()
    response = 0
    return jsonify(response), 200


# Broadcast node ring to other nodes
@app.route('/broadcast/ring', methods=['POST'])
def broadcast_ring():
    message = request.get_json()
    response = 0
    return jsonify(response), 200


# Broadcast block to other nodes
@app.route('/broadcast/block', methods=['POST'])
def broadcast_block():
    message = request.get_json()
    response = 0
    return jsonify(response), 200


# .......................................................................................
# Function for node
def start_new_node(ip, port, boot, ip_of_bootstrap, port_of_bootstrap, no_of_nodes):
    print("New node")
    new_node = Node(ip, port, boot, ip_of_bootstrap, port_of_bootstrap, no_of_nodes)


# Arguments
parser = ArgumentParser()
parser.add_argument('-ip', default='0.0.0.0', type=str, help='ip of node')
parser.add_argument('-p', '--port', default=1000, type=int, help='port to listen on')
parser.add_argument('-bootstrap', default=True, type=bool, help='is node bootstrap?')
parser.add_argument('-ip_of_bootstrap', default='0.0.0.0', type=bool, help='ip of bootstrap')
parser.add_argument('-port_of_bootstrap', default=1000, type=bool, help='port of bootstrap')
parser.add_argument('-nodes', default=5, type=int, help='number of nodes')
parser.add_argument('-cap', default=1, type=int, help='capacity of blocks')
parser.add_argument('-dif', default=4, type=int, help='difficulty')
#args = parser.parse_args()
args, _ = parser.parse_known_args()
HOST = args.ip
PORT = args.port
boot = args.bootstrap
ip_of_bootstrap = args.ip_of_bootstrap
port_of_bootstrap = args.port_of_bootstrap
no_of_nodes = args.nodes
capacity = args.cap
difficulty = args.dif
# Save HOST, PORT as cookies
# res = make_response('Setting up Cookies')
# res.set_cookie('host', HOST)
# res.set_cookie('port', PORT)


print(f'Inputs: {HOST}, {PORT}, {boot}, {ip_of_bootstrap}, {port_of_bootstrap}')
# Start node
t_node = Thread(target=start_new_node, args=(HOST, PORT, boot, ip_of_bootstrap, port_of_bootstrap, no_of_nodes))
t_node.start()


if __name__ == '__main__':
    time.sleep(2)
    # connection string to database (for user retrieval)
    #conn = ''
    # Create instance of user, each user has a wallet attached to him
    #user = Node(id=1, conn=conn)
    #print(user)
    # Start Flask app
    app.run(host=HOST, port=PORT, debug=True)
