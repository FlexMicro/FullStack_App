# FullStack_App

This repository contains a boilerplate for a containerized application. Since the focus of this is cloud deployment, the frontend and backend are left in a single file. Please note the following:

## Frontend
The frontend contains a basic React app. We are using .env to pass the API URL. Please use a .env file to consolidate the environment for deployment.

```
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000/api';
```

## Backend
There are two folders for the backend, one for Node.js and the other for Flask. Both folders showcase variables passed via the .env file. They are barebones to focus on the deployment aspect.

## Docker Compose Configuration
The `docker-compose.yml` file passes the parameters needed for this containerized application.
```
services:
  frontend:
    build: ./presentation_tier
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:3001/api
    depends_on:
      - backend

  backend:
    build: ./application_tier_flask
    ports:
      - "3001:3000"
    environment:
      - DB_HOST=${DB_HOST}
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_NAME=${DB_NAME}
```

## Environment Configuration
`env.sample` is a sample environment file. Rename it to `.env` with the correct parameters for the RDS instance and you can utilize this. This assumes your RDS is publicly accessible using your IP address.


## To Build locallly
docker-compose up


