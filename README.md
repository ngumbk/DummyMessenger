# DummyMessenger  
## О проекте  
Проект представляет из себя тестовое задание по написанию сервера, который будет обрабатывать POST-запросы и клиента, который будет отправлять запросы и тестировать пропускную способность сервера.

## Требования
Для запуска проекта на ОС Windows 10 требуется установить [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/) и [Python 3.11.4](https://www.python.org/downloads/release/python-3114/) а также иметь интернет-подключение достаточной скорости чтобы сделать пулл докер-изображений и установить зависимости.

### Используемые docker-изображения
* [MySQL](https://hub.docker.com/_/mysql/)
* [Python](https://hub.docker.com/_/python)

### Используемые порты
Приложение использует следующие порты на localhost:

| Server      | Port |
|-------------|------|
| MySQL       | 3306 |
| Server 1    | 8081 |
| Server 2    | 8082 |

## Установка проекта  
Скачайте проект с помощью [Git](http://git-scm.com/book/en/v2/Getting-Started-Installing-Git):

```sh
git clone https://github.com/ngumbk/DummyMessenger.git
```

Чтобы попасть в директорию проекта, выполните следующую команду:

```sh
cd DummyMessenger
```

Для создания виртуальной среды и установки зависимостей выполните следующую последовательность команд:

```sh
virtualenv [-p {path_to_python}] venv
./venv/Scripts/activate
python -m pip install -r requirements.txt
```

После установки Docker и зависимостей проект можно запускать.

## Запуск проекта
1. Запуск контейнеров с БД и 2 копиями веб-сервера:

    ```sh
    docker-compose up -d
    ```

    Если хотите отслеживать логи в этом же или другом терминале:

    ```sh
    docker-compose logs -f
    ```

2. Запуск клиента:  

    ```sh
    python client.py
    ```

### Остановка проекта
Чтобы остановить проект выполните следующую команду:

```sh
docker-compose down -v
```

## Возможные проблемы с запуском
### Сервер БД не успел запуститься
Возможна такая ситуация, что на вашем ПК docker-контейнер с MySQL Server запустится быстрее или медленнее, что повлечет за собой ошибку серверов, которую вы сможете отследить по логам docker-compose.  

В таком случае в docker-compose.yml увеличьте *interval* в поле *healthcheck* сервиса db_mysql примерно на то время, на которое вам нужно отсрочить запуск контейнеров с бэкенд-серверами.
```yml
...
    healthcheck:
      test: ["CMD", ...]
      timeout: 1s
      interval: 40s # Здесь добавьте ~10 секунд
      retries: 5
...
```
После внесения изменений перезапустите docker-compose.
