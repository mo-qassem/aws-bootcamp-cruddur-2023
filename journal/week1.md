# Week 1 — App Containerization
### Homework Tasks
- [x] Containerize Application (Dockerfiles, Docker Compose).
- [x] Document the Notification Endpoint for the OpenAI Document.
- [x] Write a Flask Backend Endpoint for Notifications.
- [x] Write a React Page for Notifications.
- [x] Run DynamoDB Local Container and ensure it works.
- [x] Run Postgres Container and ensure it works.

---

## 1. Containerize Application (Dockerfiles, Docker Compose).
- ### First: Create Dockerfile for both Backend-flask & Frontend-reactjs app.
  - **Create file with name of `Dockerfile` for Backend-flask app**.
  
      ```dockerfile
     FROM python:3.10-slim-buster

     WORKDIR /backend-flask

     COPY requirements.txt requirements.txt

     RUN pip3 install -r requirements.txt

     COPY . .

     ENV FLASK_ENV=development

     EXPOSE ${PORT}

     CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]
     ```
      **To build the image run..**
       ```bash
       docker build -t moqassem/cruddur-backend-flask:latest ./backend-flask
       ```
       
       
  - **Create file with name of `Dockerfile` for Frontend-reactjs App.**
  
    ```dockerfile
    FROM node:16.18

    WORKDIR /frontend-react-js

    COPY . /frontend-react-js

    RUN npm install

    ENV PORT=3000

    EXPOSE ${PORT}

    CMD ["npm", "start"]
    ```
    **To build the image run..**
    ```bash
    docker build -t moqassem/cruddur-frontend-reactjs:latest ./frontend-react-js
    ```
   
- ### Second: Create `docker-compose` file with `.yaml` extention.
  ```yaml
  version: "3.8"
  services:
    cruddur-backend-flask:
      environment:
        FRONTEND_URL: "https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
        BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
      build: ./backend-flask
      ports:
        - "4567:4567"
      volumes:
        - ./backend-flask:/backend-flask
    cruddur-frontend-reactjs:
      environment:
        REACT_APP_BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
      build: ./frontend-react-js
      ports:
        - "3000:3000"
      volumes:
        - ./frontend-react-js:/frontend-react-js
  networks: 
    internal-network:
      driver: bridge
      name: cruddur
    ```
---


## 2. Document the Notification Endpoint for the OpenAI Document.

## 3. Write a Flask Backend Endpoint for Notifications.
## 4. Write a React Page for Notifications.
## 5. Run DynamoDB Local Container and ensure it works.
## 6. Run Postgres Container and ensure it works.



---

###  Homework Challenges
- [x] Run the dockerfile CMD as an external script.
- [x] Push and tag a image to DockerHub (they have a free tier).
- [x] Use multi-stage building for a Dockerfile build.
- [x] Implement a healthcheck in the V3 Docker compose file.
- [x] Research best practices of Dockerfiles and attempt to implement it in your Dockerfile. 
- [x] Learn how to install Docker on your localmachine and get the same containers running outside of Gitpod / Codespaces.
- [x] Launch an EC2 instance that has docker installed, and pull a container to demonstrate you can run your own docker processes. 






