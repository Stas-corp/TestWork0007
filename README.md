## TestWork0007

## Description
TestWork0007 is a FastAPI based web application for task management using JWT authentication and MySQL as a database. The application supports registration, login, token update and CRUD operations for tasks.

## Functionality
- User registration and login.
- Updating access tokens.
- Create, update, delete, and search for tasks.
- Containerization using Docker Compose.

## Startup
***git and Docker should already be installed on your device***
### 1. Cloning the repository
```shell
git clone <URL of repository>
cd TestWork0007
```
### 2. Setting environment variables
Create an ***.env*** file in the root directory and add:
```shell
DB_HOST=db
MYSQL_ROOT_PASSWORD=qwerzxcv
MYSQL_DATABASE=mydb
```

### 3. Issue RSA private key + public key pair
Generate an RSA private key, of size 2048
```shell
openssl genrsa -out jwt-private.pem 2048
```
Extract the public key from the key pair, which can be used in a certificate
```shell
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```
### Files must be in the ***certs*** directory

### 4. Create and run with Docker Compose
```shell
docker compose up --build
```
The application will be accessed at: http://localhost:8000.

Documentation: http://localhost:8000/docs.
