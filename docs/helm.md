# Создание helm-шаблона приложения

## Создать базовый чарт
```shell
helm create helm-chart
```

После этого появится следующая структура:
```shell
helm-chart/
├── Chart.yaml
├── values.yaml
├── charts/
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ...
└── README.md
```

## Перенос файлов в Helm чарт
Нужно перенести файлы из директории k8s в директорию templates
```shell
helm-chart/
└── templates/
    ├── configmap.yaml
    ├── deployment.yaml
    ├── ingress.yaml
    ├── secret.yaml
    ├── service.yaml
```

Для PostgreSQL нужно создать отдельную директорию и перенести туда файлы, отвечающие за инициаллизацию БД
```shell
helm-chart/
├── Chart.yaml
├── values.yaml
├── charts/
│   └── postgresql/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── pv-pvc.yaml
│           └── storageclass.yaml
├── templates/
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── ingress.yaml
│   ├── service.yaml
│   └── secret.yaml
```

Затем, нужно добавить его как зависимость в Chart.yaml основного чарта:
```shell
dependencies:
  - name: postgresql
    version: 0.1.0
    repository: file://charts/postgresql
    condition: postgresql.enabled
    tags:
      - db-setup
```


## Шаблонизация YAML-файлов
Все .yaml файлы теперь должны быть преобразованы в шаблоны с использованием Go-шаблонизатора Helm.


## Проверка чарта
После настройки можно проверить чарт:
```shell
helm lint helm-chart
helm template helm-chart
```

## Проверить шаблон (сгененировать для визуального контроля)
```shell
helm template rel1 helm-chart -n user-crud-helm
```

## Установить зависимости
```shell
helm dependency build helm-chart
```

## Установка
```shell
helm install rel1 helm-chart -n user-crud-helm --create-namespace
```

## Удаление
```shell
helm uninstall rel1 -n user-crud-helm
```



## Ручное удаление при неудачной инсталяции
```shell
kubectl delete secret db-secret -n user-crud-helm
kubectl delete configmap app-config -n user-crud-helm
kubectl delete service user-service -n user-crud-helm
kubectl delete deployment user-app -n user-crud-helm
```

helm install rel.3 helm-chart -n user-crud-helm