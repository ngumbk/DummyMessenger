# DummyMessenger  
## Требования
Для запуска проекта на ОС Windows 10 требуется установить [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/).  
По мере разработки проекта требования будут уточняться.

## Установка проекта
Чтобы установить проект с помощью [Git](http://git-scm.com/book/en/v2/Getting-Started-Installing-Git), установите Git и следуйте следующим инструкциям:

```sh
git clone https://github.com/ngumbk/service_center_db.git
```

Чтобы попасть в директорию проекта, выполните следующую команду:

```sh
cd service_center_db
```

## Запуск проекта
1. Запуск приложения:

    ```sh
    docker-compose up -d
    ```

    **Первый запуск контейнеров может занять несколько минут...**

    ```sh
    docker-compose logs -f # Follow log output
    ```
2. Остановка приложения:

    ```sh
    docker-compose down -v
    ```
    