# Полный набор инструкций при работе с приложением

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

### Переустановка
При внесении изменений в values.yaml обновляем БД
```shell
helm upgrade db bitnami/postgresql -f k8s/postgresql/values.yaml --namespace user-crud
```

### Удаление БД
```shell
helm uninstall db --namespace user-crud
helm list --namespace user-crud
kubectl delete pvc data-db-postgresql-0 -n user-crud
```

Так как PV имеет настройку persistentVolumeReclaimPolicy: Retain (для Production) при удалении БД потребуются
дополнительные манипуляции для удаления PV и PVC.
```shell
kubectl get statefulset -n user-crud
kubectl delete statefulset <statefulset-name> -n user-crud
```

Проверка PV и PVC
```shell
kubectl get pvc data-db-postgresql-0 -n user-crud -o yaml
kubectl get pv <volume-name> -o yaml
```

Удаление Finalizers (если они есть)
```shell
kubectl patch pvc data-db-postgresql-0 -n user-crud -p '{"metadata":{"finalizers":null}}'
```

Удаление PVC
```shell
kubectl delete pvc data-db-postgresql-0 -n user-crud
```

Удаление PV (если PVC удален, но PV остался)
```shell
kubectl delete pv <volume-name>
```

Весь набор
```shell
helm uninstall db --namespace user-crud
kubectl delete pvc -n user-crud data-db-postgresql-0
kubectl delete pv <pv-name>
kubectl delete namespace user-crud
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

### Протестировать работу приложения
```shell
newman run postman-collection.json
```
Документация про Postman https://learning.postman.com/docs/tests-and-scripts/write-scripts/test-scripts/



## Доступ к БД с локального ПК
### Туннель
```shell
 kubectl port-forward --namespace user-crud svc/db-postgresql 51432:5432 &
    PGPASSWORD="$POSTGRES_PASSWORD" psql --host 127.0.0.1 -U postgres -d appdb -p 5432
```


## Заметки
### Запуск тестов приложения
```shell
PYTHONPATH=src pytest
```

### Запуск тестов приложения с выводом print из фикстур
```shell
PYTHONPATH=src pytest -s
```

### Создаение пользователя локальной БД
```shell
brew services start postgresql
createuser --superuser postgres
psql -U postgres -c "ALTER USER postgres WITH PASSWORD 'postgres';"
```

Проверка подключения
```shell
psql -h localhost -U postgres -d postgres
```

Проверка списка пользователей в БД
```shell
psql -h localhost -d postgres
\du
```

Экспорт переменных окружения для подключения к БД приложению
```shell
export DB_HOST=localhost
export DB_USER=postgres
export DB_PASSWORD=postgres
export DB_NAME=appdb
```

### Создание миграции ORM
Инициализация (один раз при создании проекта)
```shell
alembic init migrations
```

Создание актуальной версии миграции согласно текущей схеме ORM
```shell
alembic revision --autogenerate -m "Initial migration"
```

Применить миграцию в БД
```shell
alembic upgrade head
```

### Туннель в K8s БД
```shell
kubectl port-forward --namespace user-crud svc/db-postgresql 51432:5432 &              
    PGPASSWORD="$POSTGRES_PASSWORD" psql --host 127.0.0.1 -U postgres -d appdb -p 5432
```

Сбросить id
```postgresql
ALTER SEQUENCE users_id_seq RESTART;
```


### Запуск тестов Postman
Документация здесь https://learning.postman.com/docs/tests-and-scripts/write-scripts/test-scripts/
```shell
newman run postman/user_crud.postman_collection.json > user_crud.postman_collection.result.txt
```


### Памятка
* PersistentVolume — это объект Kubernetes, который предоставляет физическое хранилище для данных.
* PersistentVolumeClaim — это запрос на использование хранилища. PVC привязывается к конкретному PV.