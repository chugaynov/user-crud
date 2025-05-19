# Инструкция по запуску приложения.

## DockerHub
### Сборка приложения под AMD64
```shell
docker login
docker buildx create --use
docker buildx build --platform linux/amd64 -t achugaynov/user-crud:v1.3 . --push
```

## Установка PostgreSQL из Helm
### Установка БД
```shell
cd {user-crud-directory-path}

kubectl create namespace user-crud

kubectl apply -f k8s/postgresql/storageclass.yaml
kubectl apply -f k8s/postgresql/pv-pvc.yaml

helm repo add bitnami https://charts.bitnami.com/bitnami
helm install db bitnami/postgresql --set image.tag=16 -f k8s/postgresql/values.yaml --namespace user-crud
```

## Устновака приложения user-crud
### Примените манифесты Kubernetes
```shell
cd {user-crud-directory-path}

kubectl create namespace user-crud
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml

kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```