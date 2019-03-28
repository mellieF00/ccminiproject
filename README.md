# miniproject for Cloud Computing
This is the project for cloud computing
1, I makes use of an external REST service to provide dataset for my api, the dataset: disease.csv.  
2, The API have a sufficient set of services for the selected application domain: GET, POST, DELETE.  
3, The application uses a cloud database for accessing persistent information.  
4, The application code is well documented and with a README.md.  
5, The API has load balancing and scaling.
6, The Application has implemented hash-based authentication, also implemented user accounts and access management.

## Prerequisites
```
gcloud config set compute/zone europe-west2-b
export PROJECT_ID="$(gcloud config get-value project -q)"
```
## run your app in your vm
install the software and how to install the
```
pip install -r requirements.txt
python app.py
```

## run you app with Cassandra in Kubernetes
```
wget -O cassandra-peer-service.yml http://tinyurl.com/yyxnephy
wget -O cassandra-service.yml http://tinyurl.com/y65czz8e
wget -O cassandra-replication-controller.yml http://tinyurl.com/y2crfsl8
kubectl create -f cassandra-peer-service.yml
kubectl create -f cassandra-service.yml
kubectl create -f cassandra-replication-controller.yml
docker build -t gcr.io/${PROJECT_ID}/disease-app:v1 .
docker push gcr.io/${PROJECT_ID}/disease-app:v1
kubectl run disease-app --image=gcr.io/${PROJECT_ID}/disease-app:v1 --port 8080
kubectl expose deployment disease-app  --type=LoadBalancer --port 80 --target-port 8080
kubectl get services
```
