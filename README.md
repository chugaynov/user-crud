# Docker

## DockerHub сборка под AMD64
```shell
docker login
docker buildx create --use
docker buildx build --platform linux/amd64 -t achugaynov/user-crud:v1.0 . --push
```

## Установка БД из Helm
Если _kubectl get storageclass_ не вернул ничего, нужно добавить свой storageclass
```shell
kubectl apply -f k8s/postgresql/storageclass.yaml
```

Если динамическое provisioner'ы недоступны, создайте статический PV
```shell
kubectl apply -f k8s/postgresql/pv-pvc.yaml
```

Установка
```shell
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install db bitnami/postgresql -f k8s/postgresql/values.yaml
```

Переустановка при внесении изменений в values.yaml
```shell
helm upgrade db bitnami/postgresql -f k8s/values.yaml --install
```

Удаление
```shell
helm uninstall db
```


## Удаление
```shell
helm uninstall db
helm list
kubectl delete pvc data-db-postgresql-0 -n default
```

## Примените манифесты Kubernetes
```shell
kubectl create namespace pqsql
kubectl apply -f postgresql/k8s/storageclass.yaml
kubectl apply -f postgresql/k8s/pv-pvc.yaml
helm install db bitnami/postgresql -f postgresql/k8s/values.yaml --install --namespace pqsql


kubectl create namespace restfull-crud
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml

kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```


## Проверьте работу приложения
```shell
newman run postman-collection.json
```

## Доступ к БД с локального ПК
```shell
    kubectl port-forward --namespace pqsql svc/db-postgresql 5432:5432 &
    PGPASSWORD="$POSTGRES_PASSWORD" psql --host 127.0.0.1 -U postgres -d appdb -p 5432
```


## 
```shell
kubectl create namespace pqsql
kubectl apply -f k8s/storageclass.yaml
kubectl apply -f k8s/pv-pvc.yaml
helm upgrade db bitnami/postgresql -f k8s/values.yaml --install --namespace pqsql
```

PersistentVolume — это объект Kubernetes, который предоставляет физическое хранилище для данных.
PersistentVolumeClaim — это запрос на использование хранилища. PVC привязывается к конкретному PV.
```shell
kubectl apply -f k8s/pv-pvc.yaml
```


## 
```shell
```


# Тесты через Postman
Документация здесь https://learning.postman.com/docs/tests-and-scripts/write-scripts/test-scripts/
```shell
newman run otus-app-health.postman_collection.json
```

# Запуск теста
```shell
PYTHONPATH=src pytest
```

# Запуск теста с выводом print из фикстур
```shell
PYTHONPATH=src pytest -s
```

# Создание миграции ORM
```shell
alembic init migrations
alembic revision --autogenerate -m "Initial migration"
```