from flask import Flask,jsonify,request,render_template
from time import sleep
import os
import logging
import sys
import subprocess
import sqlite3
import requests

app = Flask(__name__)

# Créer la base pour stocker les parametres config plus-tard
DATABASE = 'mydatabase.db'


# Configurez le logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    import pyhid_usb_relay
except ModuleNotFoundError:
    logging.info("pyhid_usb_relay non trouvé, installation en cours...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyhid-usb-relay"])
    import pyhid_usb_relay


class RController:
    """Class responsible for controlling the relay."""

    def __init__(self, relay_number):
        self.Relay_Number = relay_number
        self.relay = None
        self.initialize_relay()

    def initialize_relay(self):
        """Initializes the relay device."""
        try:
            self.relay = pyhid_usb_relay.find()
            if self.relay is None:
                logging.error("Aucun relais trouvé")
        except Exception as e:
            logging.error("Exception lors de la recherche du relais : %s", e)

    def activate_relay(self, duration=1):
        """Activates the relay for a certain duration."""
        if self.relay is None:
            logging.error("Relay not initialized")
            return False

        try:
            logging.info("Activation du relais %d", self.Relay_Number)
            self.relay.set_state(self.Relay_Number, 1)  # Allumer
            sleep(duration)
            self.relay.set_state(self.Relay_Number, 0)  # Éteindre
            logging.info("Relais %d désactivé", self.Relay_Number)
            return True
        except Exception as e:
            logging.error("Échec du contrôle du relais : %s", e)
            return False

    def cleanup(self):
        """Cleans up the GPIO on exit."""
        if self.relay is not None:
            self.relay.set_state(self.Relay_Number, 0)  # Assurez-vous que le relais est éteint
            logging.info("Ressources de relais nettoyées.")

def get_relay_number():
    """Retrieve the RELAY_NUMBER from the database. If it does not exist, return 1."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT Param_Valeur FROM Parametres WHERE Param_Nom='RELAY_NUMBER'")
    result = cursor.fetchone()

    if result:
        relay_number = int(result[0])  # Get the value from the first column
    else:
        relay_number = 1  # Default value

    conn.close()
    return relay_number

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Parametres
                      (id INTEGER PRIMARY KEY, Param_Nom TEXT UNIQUE, Param_Valeur TEXT)''')
     # Insert default RELAY_NUMBER if the table is empty

    cursor.execute("SELECT COUNT(*) FROM Parametres")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute("INSERT INTO Parametres (Param_Nom, Param_Valeur) VALUES ('RELAY_NUMBER', '1')")

    conn.commit()

    conn.close()

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()
    return jsonify({'status': 'User added'})

@app.route('/set_param', methods=['POST'])
def set_param():
    """Sets a parameter in the Parametres table."""
    param_name = request.form['Param_Nom']
    param_value = request.form['Param_Valeur']

    # Check if the parameter is RELAY_NUMBER
    if param_name == 'RELAY_NUMBER':
        if param_value not in ['1', '2']:
            return jsonify({'status': 'Erreur', 'message': 'La valeur doit être 1 ou 2.'}), 400

        # Update the relay number in RController
        relay_controller.Relay_Number = int(param_value)
        logging.info(f"Relay number updated to {relay_controller.Relay_Number}")


    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Insert or update the parameter
    # Insert or update the parameter
    cursor.execute('''INSERT INTO Parametres (Param_Nom, Param_Valeur)
                      VALUES (?, ?)
                      ON CONFLICT(Param_Nom)
                      DO UPDATE SET Param_Valeur=excluded.Param_Valeur''', (param_name, param_value))

    conn.commit()
    conn.close()

    return jsonify({'status': f"Paramètre {param_name} mis à jour à {param_value}"})

@app.route('/update_relay_number', methods=['POST'])
def update_relay_number():
    """Mise à jour du RELAY_NUMBER via une requête POST."""
    new_relay_number = request.form['relay_number']

    # Check if the new relay number is either 1 or 2
    if new_relay_number not in ['1', '2']:
        return jsonify({'status': 'Erreur', 'message': 'Le numéro de relais doit être 1 ou 2.'}), 400

    # Update the RELAY_NUMBER in RController
    relay_controller.Relay_Number = int(new_relay_number)
    logging.info(f"Relay number updated to {relay_controller.Relay_Number}")


    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''UPDATE Parametres SET Param_Valeur=? WHERE Param_Nom='RELAY_NUMBER' ''',
                   (new_relay_number,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'RELAY_NUMBER updated', 'new_value': new_relay_number})

@app.route('/activate_relay', methods=['GET'])
def activate_relay():
    """Activates the relay specified by relay_number GET parameter."""
    relay_number = request.args.get('relay_number')
    if relay_number not in ['1', '2']:
        return jsonify({'status': 'Erreur', 'message': 'Le numéro de relais doit être 1 ou 2.'}), 400

    # Update the relay number in RController
    relay_controller.Relay_Number = int(relay_number)

    if relay_controller.activate_relay():
        return jsonify(message=f"Relais {relay_number} activé !"), 200
    else:
        return jsonify(message="Erreur lors de l'activation du relais."), 500

@app.route('/home')
def main_home():
    return "Hello, World!"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/on')
def turn_on():
    if relay_controller.activate_relay():
        #sleep(1.5)# Optionnel : Attendre que le relais soit actif
        return jsonify(message=f"Relais {relay_controller.Relay_Number} allumé !"), 200
    else:
        return jsonify(message="Erreur lors de l'activation du relais."), 500


@app.route('/off')
def turn_off():
    relay_controller.cleanup()
    return jsonify(message="Relais éteint !"), 200

if __name__ == '__main__':
    # Initialize the database first
    init_db()

    # Retrieve the RELAY_NUMBER from the database
    relay_number = get_relay_number()

    # Configure the relay with the retrieved number

    relay_controller = RController(relay_number)
    app.run(host='0.0.0.0')

