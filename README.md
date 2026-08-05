# Order management API

This simple API is designed for an order management system. It can serve both executors and customers. Customers can
create orders, view, edit, delete, change status, and change the executor. Executors can view orders and change
status

### Built with

- FastAPI
- asyncio
- SQLAlchemy
- Pydantic
- bcrypt
- JWT
- Swagger

### Launch

First you need to create a `.env` file based on `.env.example` with the necessary parameters

```bash
cp .env.example .env
```

If you need external access to the database, create a `docker-compose.override.yml` file with the following contents:

```yaml
services:
  db:
    ports:
      - "5432:5432"
```

Then just run Docker Compose

```bash
docker compose up -d
```

Now you can open http://127.0.0.1:8000/docs in your browser (if necessary, replace `8000` with the port you configured)

### Demonstration

You can test the API using the [interactive documentation](https://order-management-api.stepan-0x28.com/docs)

Test accounts:

| Username   | Password       | Role     |
|------------|----------------|----------|
| thomas9213 | thomas9213pass | Customer |
| josh8882   | josh8882pass   | Customer |
| kevin645   | kevin645pass   | Executor |
| james4214  | james4214pass  | Executor |
| fred4444   | fred4444pass   | Customer |
