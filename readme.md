This app contains:
- A backend container(backend in python falcon)
- A database container(database in mariadb)
- A test container

To start the backend and database just run:
```
docker-compose up
```

To run the test container which makes post requests until stopped run:
 ```
 docker-compose -f docker-compose.test.yml up
 ```

 PS: Run both commands from project root.