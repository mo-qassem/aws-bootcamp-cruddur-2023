# Week 1 — App Containerization

### Homework Tasks

- [x] Containerize Application (Dockerfiles, Docker Compose).
- [x] Document the Notification Endpoint for the OpenAI Document.
- [x] Write a Flask Backend Endpoint for Notifications.
- [x] Write a React Page for Notifications.
- [x] Run DynamoDB Local Container and ensure it works.
- [x] Run Postgres Container and ensure it works.

---

## 1. Containerize Application (Dockerfiles, Docker Compose)

- ### First: Create Dockerfile for both Backend-flask & Frontend-reactjs app

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

- ### Second: Create `docker-compose` file with `.yaml` extention

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

## 2. Document the Notification Endpoint for the OpenAPI Document

- ### What is OpenAPI Document

- #### Definition
  > The OpenAPI Specification is a standard format to define structure and syntax REST APIs. OpenAPI documents are both machine and human-readable, which enables anyone to easily determine how each API works. Engineers building APIs can use APIs to plan and design servers, generate code, and implement contract testing. Other internal teams can aggregate these API definitions to determine their API program’s footprint and dependencies.
- #### There are three primary areas in every OpenAPI document
  > - **Endpoints** (i.e. paths appended to the server URL) and the HTTP methods they support. For each method, any parameters that may or must be included in the request and the response formats for the possible HTTP response codes are specified.
  > - **Reusable components** that can be used across multiple endpoints in the API, such as common request parameters and response formats.
  > - **Meta information**, including the title, version, and description of the API, authentication method, and location of the API servers.
- ### Add the below section to `openapi-3.yaml` file to fulfill the required task

  ```yaml
  /api/activities/notifications:
  get:
    description: "Return a feed of activity for all of those that I follow"
    tags:
      - activities
    parameters: []
    responses:
    "200":
      description: Returns an array of activities
      content:
      application/json:
        schema:
        type: array
        items:
          $ref: "#/components/schemas/Activity"
  ```

## 3. Write a Flask Backend Endpoint for Notifications

- ### First: Create new `notifications_activities.py` under `backend-flask/services/`

  ```python
  from datetime import datetime, timedelta, timezone
  class NotificationsActivities:
  def run():
      now = datetime.now(timezone.utc).astimezone()
      results = [{
      'uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
      'handle':  'Mohamed Qassem',
      'message': 'Hello From Cruddur!',
      'created_at': (now - timedelta(days=2)).isoformat(),
      'expires_at': (now + timedelta(days=5)).isoformat(),
      'likes_count': 5,
      'replies_count': 1,
      'reposts_count': 0,
      'replies': [{
          'uuid': '26e12864-1c26-5c3a-9658-97a10f8fea67',
          'reply_to_activity_uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
          'handle':  'worf',
          'message': 'this post has no honor!',
          'likes_count': 10,
          'replies_count': 5,
          'reposts_count': 10,
          'created_at': (now - timedelta(days=2)).isoformat()
      }],
      }
      ]
      return results
  ```

- ### Second: Update `app.py` file with the below code

  ```python
  from services.notifications_activities import *
  ```

  ```python
  @app.route("/api/activities/notifications", methods=['GET'])
  def data_notifications():
  data = NotificationsActivities.run()
  return data, 200
  ```

## 4. Write a React Page for Notifications

- ### First: Under `frontend-react-js/src/pages/` create two new files

  - `NotificationsFeedPage.js`

    ```javascript
    import "./NotificationsFeedPage.css";
    import React from "react";

    import DesktopNavigation from "../components/DesktopNavigation";
    import DesktopSidebar from "../components/DesktopSidebar";
    import ActivityFeed from "../components/ActivityFeed";
    import ActivityForm from "../components/ActivityForm";
    import ReplyForm from "../components/ReplyForm";

    // [TODO] Authenication
    import Cookies from "js-cookie";

    export default function NotificationsFeedPage() {
      const [activities, setActivities] = React.useState([]);
      const [popped, setPopped] = React.useState(false);
      const [poppedReply, setPoppedReply] = React.useState(false);
      const [replyActivity, setReplyActivity] = React.useState({});
      const [user, setUser] = React.useState(null);
      const dataFetchedRef = React.useRef(false);

      const loadData = async () => {
        try {
          const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/notifications`;
          const res = await fetch(backend_url, {
            method: "GET",
          });
          let resJson = await res.json();
          if (res.status === 200) {
            setActivities(resJson);
          } else {
            console.log(res);
          }
        } catch (err) {
          console.log(err);
        }
      };

      const checkAuth = async () => {
        console.log("checkAuth");
        // [TODO] Authenication
        if (Cookies.get("user.logged_in")) {
          setUser({
            display_name: Cookies.get("user.name"),
            handle: Cookies.get("user.username"),
          });
        }
      };

      React.useEffect(() => {
        //prevents double call
        if (dataFetchedRef.current) return;
        dataFetchedRef.current = true;

        loadData();
        checkAuth();
      }, []);

      return (
        <article>
          <DesktopNavigation
            user={user}
            active={"notifications"}
            setPopped={setPopped}
          />
          <div className="content">
            <ActivityForm
              popped={popped}
              setPopped={setPopped}
              setActivities={setActivities}
            />
            <ReplyForm
              activity={replyActivity}
              popped={poppedReply}
              setPopped={setPoppedReply}
              setActivities={setActivities}
              activities={activities}
            />
            <ActivityFeed
              title="Notifications"
              setReplyActivity={setReplyActivity}
              setPopped={setPoppedReply}
              activities={activities}
            />
          </div>
          <DesktopSidebar user={user} />
        </article>
      );
    }
    ```

  - `NotificationsFeedPage.css`.

    ```css
    article {
      display: flex;
      flex-direction: row;
      justify-content: center;
    }
    ```

- ### Second: Update `App.js` under `frontend-react-js/src/`

  ```javascript
  import NotificationsFeedPage from "./pages/NotificationsFeedPage";
  ```

  ```javascript
  import {
  createBrowserRouter,
  RouterProvider
  } from "react-router-dom";
  const router = createBrowserRouter([
  {
    path: "/notifications",
    element: <NotificationsFeedPage />
  },
  ```

## 5. Run DynamoDB Local Container and ensure it works

- ### First: Update the `docker-compose` file

  ```yaml
  version: "3.8"
  services:
  dynamodb-local:
    user: root
    command: "-jar DynamoDBLocal.jar -sharedDb -dbPath ./data"
    image: "amazon/dynamodb-local:latest"
    container_name: dynamodb-local
    ports:
      - "8000:8000"
    volumes:
      - "./docker/dynamodb:/home/dynamodblocal/data"
    working_dir: /home/dynamodblocal
  ```

- ### Second: To make sure that it is working fine

  - #### Create dynamodb table

    ```bash
    aws dynamodb create-table \
        --endpoint-url http://localhost:8000 \
        --table-name Music \
        --attribute-definitions \
            AttributeName=Artist,AttributeType=S \
            AttributeName=SongTitle,AttributeType=S \
        --key-schema AttributeName=Artist,KeyType=HASH AttributeName=SongTitle,KeyType=RANGE \
        --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
        --table-class STANDARD
    ```

  - #### Create an Item

    ```bash
    aws dynamodb put-item \
        --endpoint-url http://localhost:8000 \
        --table-name Music \
        --item \
            '{"Artist": {"S": "No One You Know"}, "SongTitle": {"S": "Call Me Today"}, "AlbumTitle": {"S": "Somewhat Famous"}}' \
        --return-consumed-capacity TOTAL
    ```

  - #### Run

    ```bash
    aws dynamodb list-tables --endpoint-url http://localhost:8000

    aws dynamodb scan --table-name Music --query "Items" --endpoint-url http://localhost:8000
    ```

    ![response from db](/journal/screenshots/week1_db_response.png)

## 6. Run Postgres Container and ensure it works

- ### First: Update the `docker-compose` file with

  ```yaml
  version: "3.8"
  services:
  postgres-db:
      image: postgres:13-alpine
      restart: always
      environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      ports:
      - "5432:5432"
      volumes:
      - postgres-db:/var/lib/postgresql/data
  volumes:
  postgres-db:
      driver: local
  ```

- ### Second: Update `.gitpod.yaml` to install postgres client to be able to interact with postgres db server.

  ```yaml
  tasks:
    - name: Initiate Postgres client
      init: |
        curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc|sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
        echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list
        sudo apt update
        sudo apt install -y postgresql-client-13 libpq-dev
  vscode:
    extensions:
      - 42Crunch.vscode-openapi
      - cweijan.vscode-postgresql-client2
  ```

  - #### Run

  ```bash
  psql -U postgres -h localhost
  ```

  ![response from postgres](/journal/screenshots/week1_postgres.png)

---

### Homework Challenges

- [x] Run the dockerfile CMD as an external script.
- [x] Push and tag a image to DockerHub (they have a free tier).
- [x] Use multi-stage building for a Dockerfile build.
- [x] Implement a healthcheck in the V3 Docker compose file.
- [x] Research best practices of Dockerfiles and attempt to implement it in your Dockerfile.
- [x] Learn how to install Docker on your localmachine and get the same containers running outside of Gitpod / Codespaces.
- [x] Launch an EC2 instance that has docker installed, and pull a container to demonstrate you can run your own docker processes.

---

## 01. Run the dockerfile CMD as an external script.

- ### Create script file name `start-backend` under `aws-bootcamp-cruddur-2023/backend-flask`
  ```bash
  #!/bin/bash
  python3 -m flask run --host=0.0.0.0 --port=4567
  ```
- ### Update`Dockerfile` to use that script as CMD

  ```dockerfile
  FROM python:3.10-slim-buster
  WORKDIR /backend-flask
  COPY . .
  RUN pip3 install -r requirements.txt
  COPY start-backend /usr/local/bin
  RUN chmod 770 /usr/local/bin/*
  ENV FLASK_ENV=development
  EXPOSE ${PORT}
  CMD ["start-backend"]
  ```

## 02. Push and tag a image to DockerHub (they have a free tier).

- ### To login to docker-hub account locally.
  ```bash
  docker login -u (username) -p (password)
  ```
- ### To tag existing images.
  ```bash
  docker tag (existing-image-name):(existing-tag) (docker-username)/(new-image-name):(new-tag)
  ```
- ### To upload images to docker-hub.
  ```bash
  docker image push (username)/(new-image-name):(new-tag)
  ```
  ![docker-hub](/journal/screenshots/week1_docker-hub.png)

## 03. Use multi-stage building for a Dockerfile build.

- ### Create new `Dockerfile.builder`, reduce frontend image size from `1.19GB` to `412MB`.

  ```dockerfile
  FROM node:16.18 AS builder
  WORKDIR /frontend-react-js
  COPY ./frontend-react-js/ /frontend-react-js
  RUN npm install

  FROM node:alpine
  WORKDIR /frontend-app
  COPY --from=builder /frontend-react-js /frontend-app
  ENV PORT=3000
  EXPOSE ${PORT}
  CMD ["npm", "start"]
  ```

  ![docker-images](/journal/screenshots/week1_images.png)

## 04. Implement a healthcheck in the V3 Docker compose file.

- ### Update `docker-compose` with simple `crul command` to check the health of backend.

  ```yaml
  healthcheck:
    test: "curl -f http://localhost:4567/api/activites/home || exit 1"
    interval: 30s
    timeout: 10s
    retries: 2
    start_period: 30s
  ```

## 05. Research best practices of Dockerfiles and attempt to implement it in your Dockerfile.

- #### Minimize the number of layers.
  > That is what we did with multistage by offloading the heavy lifting to the first Docker image and copying the artifact to the second image with a minimal base image to lunch applications.
- #### Decouple applications.
  > Each container should have only one concern. Decoupling applications into multiple containers makes it easier to scale horizontally and reuse containers, similler like we doing with **cruddur**.

## 06. Learn how to install Docker on your localmachine and get the same containers running outside of Gitpod / Codespaces.

- ### Faced new error, solved it by add the below command to `frontend-react-js` `Dockerfile`.

```dockerfile
  RUN mkdir -p node_modules/.cache && chmod -R 777 node_modules/.cache
```

![local-deployment](/journal/screenshots/week1_local_error.png)

![local-deployment](/journal/screenshots/week1_docker_running.png)

![local-deployment](/journal/screenshots/week1_homepage.png)

![local-deployment](/journal/screenshots/week1_homepage_after_signin.png)

## 07. Launch an EC2 instance that has docker installed, and pull a container to demonstrate you can run your own docker processes.

- ### Create `cloudformation template` to bootstrap a `t2.micro` running ubuntu image to install docker & docker compose and retrieve a custom `docker-compose` file to lunch two cruddur app backend & frontend.

  ```yaml
  AWSTemplateFormatVersion: 2010-09-09
  Description: Cruddur-DEV

  Parameters:
  EnvName:
    Type: String
    Default: "Cruddur-DEV"
  InstanceAMI:
    Description: Ubuntu Image Id
    Type: String
    Default: ami-0557a15b87f6559cf
  InstanceType:
    Description: Allowed instance type to launch
    Type: String
    Default: "t2.micro"

  Resources:
  DockerHostKeyPair:
    Type: AWS::EC2::KeyPair
    Properties:
      KeyName: !Sub ${EnvName}-DockerHost-KP
      KeyType: rsa
  DockerHostInstance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: !Ref InstanceType
      ImageId: !Ref InstanceAMI
      KeyName: !Ref DockerHostKeyPair
      UserData:
        Fn::Base64: !Sub |
          #!/bin/bash
          curl -fsSL https://get.docker.com -o get-docker.sh
          sudo sh ./get-docker.sh
          sudo usermod -aG docker ubuntu
          sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
          sudo chmod +x /usr/local/bin/docker-compose
          cd home/ubuntu/
          wget https://raw.githubusercontent.com/mo-qassem/aws-bootcamp-cruddur-2023/main/journal/others/docker-compose.yaml
          docker compose up -d
      Tags:
        - Key: Name
          Value: !Sub ${EnvName}-DockerHost
  Outputs:
  DockerHostPublicIp:
    Value: !GetAtt DockerHostInstance.PublicIp
  DockerHostPairId:
    Value: !GetAtt DockerHostKeyPair.KeyPairId
  ```

- ### Delpoy it using local AWS CLI

  ```bash
  aws cloudformation create-stack --stack-name dockerhost --template-body file://cf-dockerhost.yaml  --capabilities "CAPABILITY_NAMED_IAM" --region us-east-1 --profile cruddur
  ```

  ![cloud-deployment](/journal/screenshots/week1_cloud_deploy_home.png)

  ![cloud-deployment](/journal/screenshots/week1_cloud_deploy_notif.png)

  ![cloud-deployment](/journal/screenshots/week1_cloud_deploy_console.png)
