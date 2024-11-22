from google.cloud import pubsub_v1, firestore
from django.http import JsonResponse

# Firestore setup
db = firestore.Client()

# Publish event to Pub/Sub
def publish_event(topic, message):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path('your-project-id', topic)
    publisher.publish(topic_path, message.encode("utf-8"))

# Initiate Payment
def initiate_payment(request):
    user_id = request.POST.get('user_id')
    amount = request.POST.get('amount')
    
    # Create transaction log
    transaction_id = f"txn-{uuid.uuid4()}"
    db.collection('transactions').document(transaction_id).set({
        'status': 'Initiated',
        'service': 'Initiator',
        'amount': amount,
    })
    
    # Publish initiation event
    publish_event('payment-initiation', f'{transaction_id},{amount}')
    
    return JsonResponse({'transaction_id': transaction_id, 'status': 'Initiated'})
