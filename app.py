# app.py
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Simulación de base de datos
messages = {
    'sms': [
        {'from': '123456789', 'text': 'Mensaje de prueba SMS 1', 'date': '2024-01-01 10:00'},
        {'from': '987654321', 'text': 'Mensaje de prueba SMS 2', 'date': '2024-01-01 11:00'}
    ],
    'whatsapp': [
        {'from': '123456789', 'text': 'Mensaje de prueba WhatsApp 1', 'date': '2024-01-01 12:00'},
        {'from': '987654321', 'text': 'Mensaje de prueba WhatsApp 2', 'date': '2024-01-01 13:00'}
    ],
    'facebook': [],
    'email': [],
    'calls': []
}

class Call:
    def __init__(self):
        self.active_calls = {}
    
    def start_call(self, number):
        if number not in self.active_calls:
            self.active_calls[number] = {
                'start_time': datetime.now(),
                'status': 'active',
                'muted': False,
                'on_hold': False
            }
            return True
        return False
    
    def end_call(self, number):
        if number in self.active_calls:
            del self.active_calls[number]
            return True
        return False
    
    def toggle_mute(self, number):
        if number in self.active_calls:
            self.active_calls[number]['muted'] = not self.active_calls[number]['muted']
            return True
        return False
    
    def toggle_hold(self, number):
        if number in self.active_calls:
            self.active_calls[number]['on_hold'] = not self.active_calls[number]['on_hold']
            return True
        return False

call_handler = Call()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_messages/<message_type>')
def get_messages(message_type):
    return jsonify(messages.get(message_type, []))

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    message_type = data.get('type')
    message_text = data.get('text')
    to_number = data.get('to')
    
    if message_type and message_text and to_number:
        new_message = {
            'from': 'system',
            'to': to_number,
            'text': message_text,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        messages[message_type].append(new_message)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Missing required fields'})

@app.route('/call', methods=['POST'])
def handle_call():
    data = request.json
    action = data.get('action')
    number = data.get('number')
    
    if not number:
        return jsonify({'status': 'error', 'message': 'Number is required'})
    
    if action == 'start':
        success = call_handler.start_call(number)
        return jsonify({'status': 'success' if success else 'error'})
    elif action == 'end':
        success = call_handler.end_call(number)
        return jsonify({'status': 'success' if success else 'error'})
    elif action == 'mute':
        success = call_handler.toggle_mute(number)
        return jsonify({'status': 'success' if success else 'error'})
    elif action == 'hold':
        success = call_handler.toggle_hold(number)
        return jsonify({'status': 'success' if success else 'error'})
    
    return jsonify({'status': 'error', 'message': 'Invalid action'})

if __name__ == '__main__':
    app.run(debug=True)