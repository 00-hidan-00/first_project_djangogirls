# Django application

---

## 🏗️ Preparation

Make some initialization steps. For example, copy configs.

```shell
make init-configs-i-dev
```

Initialize configs and start the development environment from scratch.

```shell
make d-dev-start
```

---

## 🐳 Docker

Use services in dockers.

### ▶️ Run

Just run

```shell
make d-run
```

### 🛫 Run detached (background)

Run services in detached mode (in the background)

```shell
make d-run-detached
```

### ⏯️ Run extended

Shutdown previous, run in detached mode, follow logs

```shell
make d-run-i-extended
```

### ⏹️Stop

Stop services

```shell
make d-stop
```

### 📜 Follow logs

Follow logs of running containers

```shell
make d-logs-follow
```

### 🚮 Purge

Purge all data related with services

```shell
make d-purge
```

### 🛠️ Apply database migrations (inside Docker container)

Apply migrations inside the running Docker container named app

```shell
make d-migrate
```

### 🆕 Create new migration files (inside Docker container)

Generate migrations inside the running Docker container named app

```shell
make d-migrations
```

---

## 🧰 Django management commands

### 🛠️ Apply database migrations (local)

Apply all pending migrations to the database

```shell
make migrate
```

### 🆕 Create new migration files (local)

Generate new migration files for changed models

```shell
make migrations
```

