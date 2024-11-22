from flask import Flask, request,jsonify
from google.cloud import pubsub_v1, firestore
import requests
import os

app = Flask(__name__)
db = firestore.Client()

@app.route('/')
def index():
    return jsonify({'message': 'Payment Processor', 'status':'Healthy. Running.'}), 200

# Subscribe to Pub/Sub
@app.route('/process-payment', methods=['POST'])
def process_payment():
    data = request.get_json()
    transaction_id, amount = data['message'].split(',')
    
    # Process payment
    try:
        # Simulate payment gateway interaction
        response = requests.post('https://payment-gateway.com/process', json={'amount': amount})
        
        if response.status_code == 200:
            # Log success
            db.collection('transactions').document(transaction_id).update({
                'status': 'Completed',
                'service': 'Processor',
            })
        else:
            raise Exception("Payment failed")
    
    except Exception as e:
        # Log failure and publish rollback
        db.collection('transactions').document(transaction_id).update({'status': 'Failed'})
        publish_event('rollback', f'{transaction_id}')
        return {'status': 'Failed'}, 500

    return {'status': 'Completed'}, 200

# Publish rollback event
def publish_event(topic, message):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path('your-project-id', topic)
    publisher.publish(topic_path, message.encode("utf-8"))

if __name__ == '__main__':
    # Fetch the port from environment variables or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
