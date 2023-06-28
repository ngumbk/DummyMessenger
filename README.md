# DummyMessenger  
## Требования
Для запуска проекта на ОС Windows 10 требуется установить [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/) и [Python 3.11.4](https://www.python.org/downloads/release/python-3114/).  
По мере разработки проекта требования будут уточняться.

## Установка проекта  
Скачайте проект с помощью [Git](http://git-scm.com/book/en/v2/Getting-Started-Installing-Git):

```sh
git clone https://github.com/ngumbk/DummyMessenger.git
```

Чтобы попасть в директорию проекта, выполните следующую команду:

```sh
cd DummyMessenger
```

Для создания виртуальной среды и установки зависимостей выполните следующий набор команд:
```sh
virtualenv [-p {path_to_python}] venv
./venv/Scripts/activate
python -m pip install -r requirements.txt
```
После установки Docker и зависимостей проект можно запускать.
## Запуск проекта
1. Запуск контейнера с БД:
    ```sh
    docker-compose up -d
    ```

    **Первый запуск контейнеров может занять несколько минут...**

    ```sh
    docker-compose logs -f # Follow log output
    ```

2. Запуск сервера:  
    ```sh
    uvicorn server:app
    ```

3. Остановка приложения:
    ```sh
    docker-compose down -v
    ```
