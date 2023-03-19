# Week 4 — Postgres and RDS

### Homework Tasks

| TASKS                                                | COMPLETED          |
| ---------------------------------------------------- | ------------------ |
| Create RDS Postgres Instance.                        | :heavy_check_mark: |
| Bash scripting for common database actions.          | :heavy_check_mark: |
| Install Postgres Driver in Backend Application.      | :heavy_check_mark: |
| Connect Gitpod to RDS Instance.                      | :heavy_check_mark: |
| Create Congito Trigger to insert user into database. | :heavy_check_mark: |
| Create new activities with a database insert.        | :heavy_check_mark: |

---

## 1. Create RDS Postgres.

- ### Use `AWS-CLI` to create RDS Instance

  ```shell
  aws rds create-db-instance \
  --db-instance-identifier cruddur-db-instance \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version  14.6 \
  --master-username cruddurroot \
  --master-user-password $AWS_POSTGRES_DB_PASSWORD \
  --allocated-storage 20 \
  --availability-zone us-east-1a \
  --backup-retention-period 0 \
  --port 5432 \
  --no-multi-az \
  --db-name cruddur \
  --storage-type gp2 \
  --publicly-accessible \
  --storage-encrypted \
  --enable-performance-insights \
  --performance-insights-retention-period 7 \
  --no-deletion-protection
  ```

  ![rds_postgres](/journal/screenshots/week4_aws_rds_postgres.png)

## 2. Bash scripting for common database actions.

- ### Create below scripts under `backend-flask/bin/`

  - `db_connect`

    ```shell
    #!/usr/bin/bash

    if [ "$1" = "prod" ];
    then
        RED='\033[0;31m'
        NO_COLOR='\033[0m'
        LABEL='USING PRODUCATION'
        printf "${RED}--- ${LABEL} ---${NO_COLOR}\n"
        URL=$PROD_CONNECTION_URL
    else
        CYAN='\033[1;36m'
        NO_COLOR='\033[0m'
        LABEL='USING LOCAL DEV'
        printf "${CYAN}--- ${LABEL} ---${NO_COLOR}\n"
        URL=$CONNECTION_URL
    fi

    psql $URL
    ```

  - `db_create`

    ```shell
    #!/usr/bin/bash
    PURPLE='\033[0;35m'
    NO_COLOR='\033[0m'
    LABEL='CREATING DATABASE'
    printf "${PURPLE}=== ${LABEL} ===${NO_COLOR}\n"

    NO_DBN_CONNECTION_URL=$(sed 's/\/cruddur//g' <<< $CONNECTION_URL)
    psql $NO_DBN_CONNECTION_URL -c 'CREATE DATABASE cruddur;'
    ```

  - `db_drop`

    ```shell
    #!/usr/bin/bash
    PURPLE='\033[0;35m'
    NO_COLOR='\033[0m'
    LABEL='DELETING DATABASE'
    printf "${PURPLE}=== ${LABEL} ===${NO_COLOR}\n"

    NO_DBN_CONNECTION_URL=$(sed 's/\/cruddur//g' <<< $CONNECTION_URL)
    psql $NO_DBN_CONNECTION_URL -c 'DROP DATABASE cruddur;'
    ```

  - `db_schema_load`

    ```shell
    #!/usr/bin/bash
    schema_path=/workspaces/aws-bootcamp-cruddur-2023/backend-flask/db/schema.sql

    PURPLE='\033[0;35m'
    NO_COLOR='\033[0m'
    LABEL='DATABASE SCHEMA LOAD'
    printf "${PURPLE}=== ${LABEL} ===${NO_COLOR}\n"

    if [ "$1" = "prod" ];
    then
        RED='\033[0;31m'
        NO_COLOR='\033[0m'
        LABEL='USING PRODUCATION'
        printf "${RED}--- ${LABEL} ---${NO_COLOR}\n"
        CON_URL=$PROD_CONNECTION_URL
    else
        CYAN='\033[1;36m'
        NO_COLOR='\033[0m'
        LABEL='USING LOCAL DEV'
        printf "${CYAN}--- ${LABEL} ---${NO_COLOR}\n"
        CON_URL=$CONNECTION_URL
    fi

    psql $CON_URL < $schema_path
    ```

  - `db_seed`

    ```shell
    #!/usr/bin/bash
    seed_path=/workspaces/aws-bootcamp-cruddur-2023/backend-flask/db/seed.sql

    PURPLE='\033[0;35m'
    NO_COLOR='\033[0m'
    LABEL='DATABASE SEED'
    printf "${PURPLE}=== ${LABEL} ===${NO_COLOR}\n"

    if [ "$1" = "prod" ];
    then
        RED='\033[0;31m'
        NO_COLOR='\033[0m'
        LABEL='USING PRODUCATION'
        printf "${RED}--- ${LABEL} ---${NO_COLOR}\n"
        CON_URL=$PROD_CONNECTION_URL
    else
        CYAN='\033[1;36m'
        NO_COLOR='\033[0m'
        LABEL='USING LOCAL DEV'
        printf "${CYAN}--- ${LABEL} ---${NO_COLOR}\n"
        CON_URL=$CONNECTION_URL
    fi

    psql $CON_URL < $seed_path
    ```

  - `db_sessions`

    ```shell
    #!/usr/bin/bash
    PURPLE='\033[0;35m'
    NO_COLOR='\033[0m'
    LABEL='DATABASE SESSIONS'
    printf "${PURPLE}=== ${LABEL} ===${NO_COLOR}\n"

    if [ "$1" = "prod" ];
    then
        RED='\033[0;31m'
        NO_COLOR='\033[0m'
        LABEL='USING PRODUCATION'
        printf "${RED}--- ${LABEL} ---${NO_COLOR}\n"
        URL=$PROD_CONNECTION_URL
    else
        CYAN='\033[1;36m'
        NO_COLOR='\033[0m'
        LABEL='USING LOCAL DEV'
        printf "${CYAN}--- ${LABEL} ---${NO_COLOR}\n"
        URL=$CONNECTION_URL
    fi

    NO_DBN_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$URL")
    psql $NO_DBN_CONNECTION_URL -c "select pid as process_id, \
          usename as user,  \
          datname as db, \
          client_addr, \
          application_name as app,\
          state \
    from pg_stat_activity;"
    ```

  - `db_setup`

    ```shell
    #!/usr/bin/bash
    set -e
    PURPLE='\033[0;35m'
    NO_COLOR='\033[0m'
    LABEL='DATABASE SETUP'
    printf "${PURPLE}=== ${LABEL} ===${NO_COLOR}\n"

    bin_path=/workspaces/aws-bootcamp-cruddur-2023/backend-flask/bin/

    source "$bin_path/db_drop"
    source "$bin_path/db_create"
    source "$bin_path/db_schema_load"
    source "$bin_path/db_seed"
    ```

- ### Create below `SQL` files under `backend-flask/db/`

  - `schema.sql`

    ```sql
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

    DROP TABLE IF EXISTS public.users;
    DROP TABLE IF EXISTS public.activities;

    CREATE TABLE public.users (
    uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    display_name text,
    handle text,
    cognito_user_id text,
    created_at TIMESTAMP default current_timestamp NOT NULL
    );

    CREATE TABLE public.activities (
    uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_uuid UUID NOT NULL,
    message text NOT NULL,
    replies_count integer DEFAULT 0,
    reposts_count integer DEFAULT 0,
    likes_count integer DEFAULT 0,
    reply_to_activity_uuid integer,
    expires_at TIMESTAMP,
    created_at TIMESTAMP default current_timestamp NOT NULL
    );
    ```

  - `seed.sql`

    ```sql
    INSERT INTO public.users (display_name, handle, cognito_user_id)
    VALUES
    ('Andrew Brown', 'andrewbrown' ,'MOCK'),
    ('Andrew Bayko', 'bayko' ,'MOCK');

    INSERT INTO public.activities (user_uuid, message, expires_at)
    VALUES
    (
        (SELECT uuid from public.users WHERE users.handle = 'andrewbrown' LIMIT 1),
        'This was imported as seed data!',
        current_timestamp + interval '10 day'
    )
    ```

## 03. Install Postgres Driver in Backend Application.

- ### Add below python libraries to `requirements.txt` and install them.

  ```shell
  psycopg[binary]
  psycopg[pool]
  ```

- ### Create two functions under `backend-flask/lib/db.py` to create `Connection Pool` and return raw json data from database.

  ```python
  from psycopg_pool import ConnectionPool
  import os

  def query_wrap_object(template):
    sql = f"""
    (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
    {template}
    ) object_row);
    """
    return sql

  def query_wrap_array(template):
    sql = f"""
    (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
    {template}
    ) array_row);
    """
    return sql

  connection_url = os.getenv("CONNECTION_URL")
  pool = ConnectionPool(connection_url)
  ```

- ### Update and add env-vars for `cruddur-backend-flask` service in `docker-compose.yaml`

  ```yaml
  CONNECTION_URL: "${DEV_CONNECTION_URL}"
  ```

- ### Update `home_activities.py` main function to load mock data from local PostgreSQL DB or real data from API call.

  ```python
  #---------COnfigure postgres pool-----------------
  from lib.db import pool, query_wrap_array
  ```

  ```python
  class HomeActivities:
  def run(Logger, cognito_user_id=None):
  #----------------Fetch Data from Postgres DB----------------
    sql = query_wrap_array("""
      SELECT
        activities.uuid,
        users.display_name,
        users.handle,
        activities.message,
        activities.replies_count,
        activities.reposts_count,
        activities.likes_count,
        activities.reply_to_activity_uuid,
        activities.expires_at,
        activities.created_at
      FROM public.activities
      LEFT JOIN public.users ON users.uuid = activities.user_uuid
      ORDER BY activities.created_at DESC
      """)
    with pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(sql)
        # this will return a tuple
        # the first field being the data
        json = cur.fetchone()
        #json = cur.fetchall()
    return json[0]
  ```

  ![sql_home](/journal/screenshots/week4_home_using_sqlfetch.png)

## 04. Connect `local Dev-Env Public Ip` to RDS Instance.

- ### Export below env-vars
  ```shell
  local_DevEnv_PublicIp=$(curl ifconfig.me.)
  DB_SG_ID=sg-001751bca040b1d2b
  DB_SG_RULE_ID=sgr-00e47810964b08426
  ```
- ### Update RDS SG using below CMD using AWS-CLI

  ```shell
  aws ec2 modify-security-group-rules \
      --group-id $DB_SG_ID \
      --security-group-rules "SecurityGroupRuleId=$DB_SG_RULE_ID,SecurityGroupRule={Description=local_DevEnv,IpProtocol=tcp,FromPort=5432,ToPort=5432,CidrIpv4=$local_DevEnv_PublicIp/32}"
  ```

- ### Create `rds_update_sg` script under `backend-flask/bin/` to automate the update each time start Dev-Container Envirment.

  ```shell
  #!/usr/bin/bash
  set -e
  PURPLE='\033[0;35m'
  NO_COLOR='\033[0m'
  LABEL='UPDATE AWS-RDS SECUIRTY GROUP RULE'
  printf "${PURPLE}=== ${LABEL} ===${NO_COLOR}\n"

  RED='\033[0;31m'
  NO_COLOR='\033[0m'
  LABEL='GETTING PUBLIC IP ADDRESS'
  printf "${RED}--- ${LABEL} ---${NO_COLOR}\n"
  source /workspaces/aws-bootcamp-cruddur-2023/.devcontainer/.env
  echo ""
  echo "Public-IP: $local_DevEnv_PublicIp"
  echo""

  /usr/local/bin/aws ec2 modify-security-group-rules \
        --group-id $DB_SG_ID \
        --security-group-rules "SecurityGroupRuleId=$DB_SG_RULE_ID,SecurityGroupRule={Description=DevEnv_PublicIP,IpProtocol=tcp,FromPort=5432,ToPort=5432,CidrIpv4=$local_DevEnv_PublicIp/32}" --no-paginate
  ```

- ### Update `devcontainer.json` to run `rds_update_sg` each time start Dev-Container Envirment

```json
  "postAttachCommand": "cd ./frontend-react-js && npm install && cd ../backend-flask && pip install -r requirements.txt --no-warn-script-location && export PATH='/home/cruddur/.local/bin:$PATH' && /usr/bin/chmod u+x /workspaces/aws-bootcamp-cruddur-2023/backend-flask/bin/* && /usr/bin/bash /workspaces/aws-bootcamp-cruddur-2023/backend-flask/bin/rds_update_sg "
```
