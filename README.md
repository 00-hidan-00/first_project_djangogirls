# Django Blog Project 📝

![CI Pipeline](https://github.com/00-hidan-00/first_project_djangogirls/actions/workflows/main-workflow.yml/badge.svg)


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

## ⚡ Quick Start

Start the full development environment (Docker-based):

```shell
make init-configs-local-dev
make d-run-extended-full-dev
```

---

## 🖥️ Local Development (locally)

### ▶️ Run Django development server

Runs the Django dev server using your local virtual environment.

```shell
make runserver
```

> Requires the PostgreSQL service to be running via:
>```shell
>make d-run-local-dev
>```

### 📦 Apply migrations

Applies all pending database migrations outside Docker.

```shell
make migrate
```

### 🧾 Create migrations

Creates new Django migration files based on model changes (no Docker involved).

```shell
make migrations
```

### 👤 Create superuser

Creates a Django superuser locally if it doesn't already exist.

```shell
make init-dev-create-superuser
```

Default Superuser Credentials:
> Username: admin
>
>Email: admin@example.com
>
>Password: admin

---

## 🐳 Full Development (with Docker)

### ▶️ Start `local_dev` environment (PostgreSQL)

Runs only the PostgreSQL container using the `local_dev` Docker profile.

```shell
make d-run-local-dev
```

### ⛔ Stop `local_dev` environment

Stops all containers from the `local_dev` profile.

```shell
make d-stop-local-dev
```

### 🧼 Purge `local_dev` environment

Removes local containers, volumes, and images used in `local_dev`.

```shell
make d-purge-local-dev
```

### ▶️ Start `full_dev` environment (Django, PostgreSQL)

Builds and runs all services defined in the `full_dev` Docker profile.

```shell
make d-run-full-dev
```

### ⏯️ Extended `full_dev` start

Stops previous containers, restarts everything in detached mode, and follows logs.

```shell
make d-run-extended-full-dev
```

### ⛔ Stop `full_dev` environment

Stops all containers from the `full_dev` profile.

```shell
make d-stop-full-dev
```

### 🧼 Purge `full_dev` environment

Removes containers, volumes, and images used in `full_dev`.

```shell
make d-purge-full-dev
```

### 📜 Follow Docker logs `full_dev`

Tails logs from all containers running in `full_dev`.

```shell
make d-logs-follow-full_dev
```

### 📦 Apply migrations (inside container)

Applies database migrations inside the `app` Docker container.

```shell
make d-migrate
```

### 🧾 Create migrations (inside container)

Creates migration files inside the `app` container.

```shell
make d-migrations
```

### 👤 Create superuser (inside container)

Creates a Django superuser inside the `app` container if one doesn't exist.

```shell
make d-init-dev-create-superuser
```

Default Superuser Credentials:
> Username: admin
>
>Email: admin@example.com
>
>Password: admin

---

## 📎 License

This project is for educational purposes.

---