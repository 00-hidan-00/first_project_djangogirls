# Django Blog Project 📝

### 🌟 Overview

This is a learning project inspired by the [Django Girls tutorial](https://tutorial.djangogirls.org/en/).
Initially designed as a beginner-friendly blog, the project has been **refactored and modernized** to follow best
practices in Django development.

- 🧱 Django Models with Admin Panel Integration
- 🔀 Clean URL routing and modular views
- ⚙️ Generic Class-Based Views (`ListView`, `DetailView`, etc.)
- 🎨 Dynamic HTML templates with CSS styling
- 📝 Form building and handling
- 🧠 Django ORM with custom QuerySets and filtering

---

## 🏗️ Preparation

Make sure to copy configuration files before starting the environment:

```shell
make init-configs-i-dev
```

Start the local development environment from scratch:

```shell
make d-dev-start
```

---

## 🐳 Docker

This project uses Docker and `Makefile` commands for streamlined development.

### ▶️ Run

Start all Docker services:

```shell
make d-run
```

### ⏯️ Extended Run

Shut down previous containers, run in detached mode, and follow logs:

```shell
make d-run-i-extended
```

### ⏹️ Stop Services

Gracefully stop running services:

```shell
make d-stop
```

### 📜 View Logs

Tail logs from running containers:

```shell
make d-logs-follow
```

### 🚮 Purge Environment

Remove all Docker volumes, containers, and networks:

```shell
make d-purge
```

### 👤 Create Superuser

Automatically creates a superuser with default credentials if it doesn't already exist:

```shell
make init-dev-i-create-superuser
```

Default credentials:
> Username: admin
>
>Email: admin@example.com
>
>Password: admin

### 🛠️ Apply Migrations

Apply all pending database migrations inside the container:

```shell
make d-migrate
```

### 🆕 Create Migration Files

Generate migration files inside the container:

```shell
make d-migrations
```

---

## 🧰 Django Management (Local)

> Useful when working without Docker.

### 🛠️ Apply Migrations Locally

```shell
make migrate
```

### 🆕 Create Migration Files Locally

```shell
make migrations
```

---

## 📎 License

This project is for educational purposes.