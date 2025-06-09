
## 1. Create Environment Configuration

### Copy the example environment file to create your own `.env` file:

```
cp .env.example .env
```

### Configure the .env file with the necessary values:

```
# ==============================
# Server Configuration
# ==============================
DOMAIN_URL=
FRONTEND_URL=
PORT=4057

# ==============================
# PostgreSQL Configuration
# ==============================
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_USERNAME=
POSTGRES_PASSWORD=
POSTGRES_DATABASE_NAME=
PG_CONN_STR=
# ==============================
# Verification-Token Configuration
# ==============================
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=

# ==============================
# Email Configuration
# ==============================
EMAIL_USERNAME=
EMAIL_HOST=
EMAIL_PORT=
EMAIL_PASSWORD=
EMAIL_FROM=
MAIL_STARTTLS=
MAIL_SSL_TLS=
USE_CREDENTIALS=
VALIDATE_CERTS=

```


## 2. Run training_model.py 
```
python training_model.py
```

## 3. Install Python Dependencies
### Ensure you have all required Python dependencies installed:

```
pip install -r requirements.txt
```

## 4. Apply Database Migrations

### Before starting the server, apply database migrations:

```
alembic upgrade head
```

