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
    psql $CONNECTION_URL
    ```
  - `db_create`

    ```shell
    #!/usr/bin/bash
    CYAN='\033[1;36m'
    NO_COLOR='\033[0m'
    LABEL='CREATING DATABASE'
    printf "${CYAN}== ${LABEL} ==${NO_COLOR}\n"

    NO_DBN_CONNECTION_URL=$(sed 's/\/cruddur//g' <<< $CONNECTION_URL)
    psql $NO_DBN_CONNECTION_URL -c 'CREATE DATABASE cruddur;'
    ```

  - `db_drop`

    ```shell
    #!/usr/bin/bash
    CYAN='\033[1;36m'
    NO_COLOR='\033[0m'
    LABEL='DELETING DATABASE'
    printf "${CYAN}== ${LABEL} ==${NO_COLOR}\n"

    NO_DBN_CONNECTION_URL=$(sed 's/\/cruddur//g' <<< $CONNECTION_URL)
    psql $NO_DBN_CONNECTION_URL -c 'DROP DATABASE cruddur;'
    ```

  - `db_schema_load`

    ```shell
    #!/usr/bin/bash
    schema_path=/workspaces/aws-bootcamp-cruddur-2023/backend-flask/db/schema.sql

    CYAN='\033[1;36m'
    NO_COLOR='\033[0m'
    LABEL='DATABASE SCHEMA LOAD'
    printf "${CYAN}== ${LABEL} ==${NO_COLOR}\n"

    if [ $1 = 'prod' ];
    then
        echo "USING PRODUCATION"
        CON_URL=$PROD_CONNECTION_URL
    else
        echo "USING LOCAL DEV"
        CON_URL=$CONNECTION_URL
    fi

    psql $CON_URL < $schema_path
    ```

  - `db_seed`

    ```shell
    #!/usr/bin/bash
    seed_path=/workspaces/aws-bootcamp-cruddur-2023/backend-flask/db/seed.sql

    CYAN='\033[1;36m'
    NO_COLOR='\033[0m'
    LABEL='DATABASE SEED'
    printf "${CYAN}== ${LABEL} ==${NO_COLOR}\n"

    if [ $1 = 'prod' ];
    then
        echo "USING PRODUCATION"
        CON_URL=$PROD_CONNECTION_URL
    else
        echo "USING LOCAL DEV"
        CON_URL=$CONNECTION_URL
    fi

    psql $CON_URL < $seed_path
    ```

- ### Create below sql files under `backend-flask/db/`

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
