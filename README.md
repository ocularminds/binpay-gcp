# **BinPay - GCP Based Microservices Payment Solution**

## **Overview**
This project is a microservices-based payment solution implemented using Python, Django, and Flask. The architecture follows the Saga pattern to ensure distributed transaction management with rollback capabilities. It uses Google Cloud Platform (GCP) for deployment, leveraging Pub/Sub for messaging, Firestore for transaction logging, and options for deployment via Cloud Run or Kubernetes (GKE).

---

## **Table of Contents**
1. [Architecture](#architecture)
2. [Setup](#setup)
3. [Testing](#testing)
4. [Continuous Integration and Deployment (CI/CD)](#ci-cd)
5. [Deployment on GCP](#deployment-on-gcp)
   - [Cloud Run](#cloud-run)
   - [Google Kubernetes Engine (GKE)](#gke)
6. [Usage](#usage)

---

## **Architecture**
- **Services**:
  - **Initiator**: Handles user management and payment initiation.
  - **Processor**: Processes payments, logs distributed transactions, and handles rollbacks.
- **GCP Components**:
  - **Pub/Sub**: Event-driven communication between microservices.
  - **Firestore**: Central transaction logging.
  - **Deployment**: Cloud Run or GKE for service orchestration.

---

## **Setup**

### **1. Prerequisites**
- Python 3.8+
- Google Cloud SDK
- Docker
- Kubernetes (kubectl)
- Terraform (optional, for infrastructure as code)

### **2. Clone the Repository**
```bash
git clone https://github.com/your-repo/binpay-gcp.git
cd binpay-gcp
```

### **3. Install Dependencies**
For Initiator
```bash
cd initiator
pip install -r requirements.txt
```

For Processor:

bash
```bash
cd processor
pip install -r requirements.txt
```
4. Set Up GCP Project
Enable the following APIs:
Pub/Sub
Firestore
Cloud Run
Kubernetes Engine

Create a Firestore database in Native mode:
```bash
gcloud firestore databases create --region=<region>
```
5. Environment Variables
Create a .env file for each service with the following:
```bash
env
# Common
PROJECT_ID=your-gcp-project-id
PUBSUB_TOPIC=binpay-initiation
PUBSUB_ROLLBACK_TOPIC=rollback

# Django Specific
DJANGO_SECRET_KEY=your-secret-key

# Flask Specific
PAYMENT_GATEWAY_URL=https://your-payment-gateway.com
```

6. Dockerize the Services
For Initiator:

```bash
cd initiator
docker build -t gcr.io/your-gcp-project-id/initiator .
```

For Processor:
```bash
cd processor
docker build -t gcr.io/your-gcp-project-id/processor .
```

Push the images:
```bash
docker push gcr.io/your-gcp-project-id/initiator
docker push gcr.io/your-gcp-project-id/processor
```

## Testing
### Unit Testing
Run tests for each service:

Payment Initiator Service:
```bash
python manage.py test
```

Payment Processor Service:
```bash
pytest
```

### Integration Testing
Simulate end-to-end transaction scenarios:

Initiate a payment request from the Initiator service.
Verify the Processor service processes the payment and logs transactions in Firestore.
Simulate a failure in the Processor service and validate rollback behavior.

CI/CD
1. Set Up CI/CD Pipeline
Use GitHub Actions or GitLab CI/CD for automation.

Deployment on GCP
Cloud Run
Deploy Services

```bash
gcloud run deploy initiator \
    --image gcr.io/your-gcp-project-id/initiator \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated

gcloud run deploy processor \
    --image gcr.io/your-gcp-project-id/processor \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

Set Up Pub/Sub Triggers
Create subscriptions for topics:
```bash
gcloud pubsub subscriptions create initiator-sub \
    --topic=binpay-initiation

gcloud pubsub subscriptions create processor-sub \
    --topic=rollback
```
Link Subscriptions to Cloud Run

```bash
gcloud run services add-iam-policy-binding initiator \
    --member=serviceAccount:your-service-account \
    --role=roles/pubsub.subscriber
```
Google Kubernetes Engine (GKE)
Set Up GKE Cluster

```bash
gcloud container clusters create binpay-cluster \
    --region us-central1 \
    --num-nodes 3
```
## Deploy Services

Apply Kubernetes manifests (k8s/initiator.yaml, k8s/processor.yaml):
```bash
kubectl apply -f k8s/initiator.yaml
kubectl apply -f k8s/processor.yaml
Set Up Pub/Sub with Kubernetes
```

Use the Pub/Sub Kubernetes Connector to link Pub/Sub topics to Kubernetes services.
Monitor Services

Use GCP Cloud Monitoring and Logging for real-time performance tracking.

## Usage
Initiate Payment
Send a POST request to the Initiator service:

```bash
curl -X POST -d "user_id=1&amount=100.00" http://<initiator-url>/initiate-payment
```

Simulate Rollback
Trigger a failure in the Processor service and observe rollback actions logged in Firestore.

## Contributing
Fork the repository.
Create a feature branch.
Commit your changes.
Submit a pull request.
License
This project is licensed under the MIT License. See the LICENSE file for details.

## Deployment Notes:
For initiator:
Use ```python manage.py runserver``` for local development.

For processor:
Use ```python app.py``` for local development, or deploy using Gunicorn for production:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```









