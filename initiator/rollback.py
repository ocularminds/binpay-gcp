# Handle rollback event
@app.route('/rollback', methods=['POST'])
def rollback_transaction():
    data = request.get_json()
    transaction_id = data['message']
    
    # Retrieve transaction log
    transaction = db.collection('transactions').document(transaction_id).get().to_dict()
    
    # Perform compensating actions
    if transaction and transaction['status'] != 'Rolled Back':
        # Example: Reverse account debit
        reverse_debit(transaction_id)
        
        # Update log
        db.collection('transactions').document(transaction_id).update({'status': 'Rolled Back'})
    
    return {'status': 'Rolled Back'}, 200

def reverse_debit(transaction_id):
    # Logic to reverse payment (e.g., update database)
    print(f"Reversing payment for transaction {transaction_id}")
