from flask import Flask, request, jsonify, send_from_directory
import requests,os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

well_known_dir = os.path.join(app.root_path, '.well-known')

class CurrencyConverterPlugin:
    def __init__(self):
        self.api_url = 'https://api.exchangerate-api.com/v4/latest/USD'  # API URL for getting exchange rates

    def get_exchange_rate(self, from_currency, to_currency):
        response = requests.get(self.api_url)
        data = response.json()

        if from_currency not in data['rates'] or to_currency not in data['rates']:
            return None

        from_rate = data['rates'][from_currency]
        to_rate = data['rates'][to_currency]

        return to_rate / from_rate

    def convert(self, amount, from_currency, to_currency):
        exchange_rate = self.get_exchange_rate(from_currency, to_currency)

        if exchange_rate is None:
            return None

        return amount * exchange_rate

@app.route('/.well-known/<path:filename>')
def well_known(filename):
    return send_from_directory(well_known_dir, filename)
    
@app.route('/convert', methods=['GET'])
def convert_currency():
    amount = float(request.args.get('amount'))
    from_currency = request.args.get('from_currency')
    to_currency = request.args.get('to_currency')

    converter = CurrencyConverterPlugin()
    converted_amount = converter.convert(amount, from_currency, to_currency)

    if converted_amount is None:
        return jsonify({'error': 'Conversion failed. Please check your input.'}), 400

    return jsonify({'converted_amount': converted_amount})

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=3333)


