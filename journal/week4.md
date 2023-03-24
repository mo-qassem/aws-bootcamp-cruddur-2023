# Week 4 — Postgres and RDS

### Homework Tasks

| VIDEOS                                                                                                                                    | WATCHED            |
| ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| [Ashish's Week 4 - Security Considerations](https://www.youtube.com/watch?v=UourWxz7iQg&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=45) | :heavy_check_mark: |

| TASKS                                                                                                           | COMPLETED          |
| --------------------------------------------------------------------------------------------------------------- | ------------------ |
| [Create RDS Postgres Instance.](#1-create-rds-postgres)                                                         | :heavy_check_mark: |
| [Bash scripting for common database actions.](#2-bash-scripting-for-common-database-actions)                    | :heavy_check_mark: |
| [Install Postgres Driver in Backend Application.](#03-install-postgres-driver-in-backend-application)           | :heavy_check_mark: |
| [Connect Gitpod to RDS Instance.](#04-connect-local-dev-env-public-ip-to-rds-instance)                          | :heavy_check_mark: |
| [Create Cognito Trigger to insert user into database.](#05-create-cognito-trigger-to-insert-user-into-database) | :heavy_check_mark: |
| [Create new activities with a database insert.](#06-create-new-activities-with-a-database-insert)               | :heavy_check_mark: |

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
        LABEL='USING PRODUCTION'
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
        LABEL='USING PRODUCTION'
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
        LABEL='USING PRODUCTION'
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
        LABEL='USING PRODUCTION'
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
      display_name text NOT NULL,
      handle text NOT NULL,
      email text NOT NULL,
      cognito_user_id text NOT NULL,
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
    INSERT INTO public.users (display_name, email, handle, cognito_user_id)
    VALUES
      ('Andrew Brown','andrew@exampro.co' , 'andrewbrown' ,'MOCK'),
      ('Andrew Bayko','bayko@exampro.co' , 'bayko' ,'MOCK'),
      ('Londo Mollari', 'lmollari@centari.com','londo','MOCK');

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

- ### Create `rds_update_sg` script under `backend-flask/bin/` to automate the update each time start Dev-Container Environment.

  ```shell
  #!/usr/bin/bash
  set -e
  PURPLE='\033[0;35m'
  NO_COLOR='\033[0m'
  LABEL='UPDATE AWS-RDS SECURITY GROUP RULE'
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

- ### Update `devcontainer.json` to run `rds_update_sg` each time start Dev-Container Environment

  ```json
  "postAttachCommand": "cd ./frontend-react-js && npm install && cd ../backend-flask && pip install -r requirements.txt --no-warn-script-location && export PATH='/home/cruddur/.local/bin:$PATH' && /usr/bin/chmod u+x /workspaces/aws-bootcamp-cruddur-2023/backend-flask/bin/* && /usr/bin/bash /workspaces/aws-bootcamp-cruddur-2023/backend-flask/bin/rds_update_sg "
  ```

## 05. Create Cognito Trigger to insert user into database.

- ### Update `schema.sql` and add additional attributes to `users` table

  ```sql
  CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

  DROP TABLE IF EXISTS public.users;
  DROP TABLE IF EXISTS public.activities;

  CREATE TABLE public.users (
    uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    display_name text NOT NULL,
    handle text NOT NULL,
    email text NOT NULL,
    cognito_user_id text NOT NULL,
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

- ### Create lambda function to be triggered by AWS Cognito and add user info to RDS-DB

  - Update lambda execution role and add the permission for CreateNetworkInterface by adding inline policy include the below actions.
    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "ec2:DescribeNetworkInterfaces",
            "ec2:CreateNetworkInterface",
            "ec2:DeleteNetworkInterface",
            "ec2:DescribeInstances",
            "ec2:AttachNetworkInterface"
          ],
          "Resource": "*"
        }
      ]
    }
    ```
  - Add below ENV-VAR to make our lambda code able to connect to our RDS-DB
    ```
    CONNECTION_URL=postgres://****:****@cruddur-db-instance.****.us-east-1.rds.amazonaws.com:5432/****
    ```
  - Add below `lambda layer` to make lambda use the Postgres Driver library in our code
    ```shell
    arn:aws:lambda:us-east-1:898466741470:layer:psycopg2-py38:2
    ```
  - Deploy lambda inside the same RDS-DB VPC by changing lambda VPC setting to be able to communicate with our DB.
  - Update lambda_function.py with

    ```python
    import os
    import json
    import psycopg2

    def lambda_handler(event, context):
        user = event['request']['userAttributes']
        user_display_name = user['name']
        user_email = user['email']
        user_handle = user['preferred_username']
        user_cognito_id = user['sub']
        try:
            conn = psycopg2.connect(os.getenv('CONNECTION_URL'))
            cur = conn.cursor()

            sql = f"""
            INSERT INTO public.users (display_name, email, handle, cognito_user_id)
            VALUES('{user_display_name}', '{user_email}', '{user_handle}', '{user_cognito_id}')
            """
            cur.execute(sql)
            conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                cur.close()
                conn.close()
                print('Database connection closed.')

        return event
    ```

  - Add Lambda triggers to our cognito user pool to be triggered when user `SignUp` with `Post confirmation trigger`.

## 06. Create new activities with a database insert
  - ### Refactor

  ```python
  from psycopg_pool import ConnectionPool
  import os
  import re
  import sys
  from flask import current_app as app

  class Db:
    def __init__(self):
      self.init_pool()

    def template(self,*args):
      pathing = list((app.root_path,'db','sql',) + args)
      pathing[-1] = pathing[-1] + ".sql"

      template_path = os.path.join(*pathing)

      green = '\033[92m'
      no_color = '\033[0m'
      print("\n")
      print(f'{green} Load SQL Template: {template_path} {no_color}')

      with open(template_path, 'r') as f:
        template_content = f.read()
      return template_content

    def init_pool(self):
      connection_url = os.getenv("CONNECTION_URL")
      self.pool = ConnectionPool(connection_url)
    # we want to commit data such as an insert
    # be sure to check for RETURNING in all uppercases
    def print_params(self,params):
      blue = '\033[94m'
      no_color = '\033[0m'
      print(f'{blue} SQL Params:{no_color}')
      for key, value in params.items():
        print(key, ":", value)

    def print_sql(self,title,sql,params={}):
      cyan = '\033[96m'
      no_color = '\033[0m'
      print(f'{cyan} SQL STATEMENT-[{title}]------{no_color}')
      print(sql,params)
    def query_commit(self,sql,params={}):
      self.print_sql('commit with returning',sql,params)

      pattern = r"\bRETURNING\b"
      is_returning_id = re.search(pattern, sql)

      try:
        with self.pool.connection() as conn:
          cur =  conn.cursor()
          cur.execute(sql, params)
          if is_returning_id:
            returning_id = cur.fetchone()[0]
          conn.commit() 
          if is_returning_id:
            return returning_id
      except Exception as err:
        self.print_sql_err(err)
    # when we want to return a a single value
    def query_value(self,sql,params={}):
      self.print_sql('value',sql,params)

      with self.pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql,params)
          json = cur.fetchone()
          return json[0]
    # when we want to return a json object
    def query_array_json(self,sql,params={}):
      self.print_sql('array',sql,params)

      wrapped_sql = self.query_wrap_array(sql)
      with self.pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(wrapped_sql,params)
          json = cur.fetchone()
          return json[0]
    # When we want to return an array of json objects
    def query_object_json(self,sql,params={}):
      self.print_sql('json',sql,params)
      self.print_params(params)
      wrapped_sql = self.query_wrap_object(sql)

      with self.pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(wrapped_sql,params)
          json = cur.fetchone()
          if json == None:
            "{}"
          else:
            return json[0]
    def query_wrap_object(self,template):
      sql = f"""
      (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
      {template}
      ) object_row);
      """
      return sql
    def query_wrap_array(self,template):
      sql = f"""
      (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
      {template}
      ) array_row);
      """
      return sql
    def print_sql_err(self,err):
      # get details about the exception
      err_type, err_obj, traceback = sys.exc_info()

      # get the line number when exception occured
      line_num = traceback.tb_lineno

      # print the connect() error
      print ("\npsycopg ERROR:", err, "on line number:", line_num)
      print ("psycopg traceback:", traceback, "-- type:", err_type)

      # print the pgcode and pgerror exceptions
      print ("pgerror:", err.pgerror)
      print ("pgcode:", err.pgcode, "\n")

  db = Db()
  ```
  - ### Create
  ```sql
  INSERT INTO public.activities (
  user_uuid,
  message,
  expires_at
)
VALUES (
  (SELECT uuid 
    FROM public.users 
    WHERE users.handle = %(handle)s
    LIMIT 1
  ),
  %(message)s,
  %(expires_at)s
) RETURNING uuid;
```
```sql
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
```
```sql
SELECT
  activities.uuid,
  users.display_name,
  users.handle,
  activities.message,
  activities.created_at,
  activities.expires_at
FROM public.activities
INNER JOIN public.users ON users.uuid = activities.user_uuid 
WHERE 
  activities.uuid = %(uuid)s
```
  - ### Refactor
  ```python
  from datetime import datetime, timedelta, timezone

  from lib.db import db

  class CreateActivity:
    def run(message, user_handle, ttl):
      model = {
        'errors': None,
        'data': None
      }

      now = datetime.now(timezone.utc).astimezone()

      if (ttl == '30-days'):
        ttl_offset = timedelta(days=30) 
      elif (ttl == '7-days'):
        ttl_offset = timedelta(days=7) 
      elif (ttl == '3-days'):
        ttl_offset = timedelta(days=3) 
      elif (ttl == '1-day'):
        ttl_offset = timedelta(days=1) 
      elif (ttl == '12-hours'):
        ttl_offset = timedelta(hours=12) 
      elif (ttl == '3-hours'):
        ttl_offset = timedelta(hours=3) 
      elif (ttl == '1-hour'):
        ttl_offset = timedelta(hours=1) 
      else:
        model['errors'] = ['ttl_blank']

      if user_handle == None or len(user_handle) < 1:
        model['errors'] = ['user_handle_blank']

      if message == None or len(message) < 1:
        model['errors'] = ['message_blank'] 
      elif len(message) > 280:
        model['errors'] = ['message_exceed_max_chars'] 

      if model['errors']:
        model['data'] = {
          'handle':  user_handle,
          'message': message
        }   
      else:
        expires_at = (now + ttl_offset)
        uuid = CreateActivity.create_activity(user_handle, message, expires_at)
        object_json = CreateActivity.query_object_activity(uuid)
        model['data'] = object_json
      return model

    def create_activity(handle, message, expires_at):
      sql = db.template('activities','create')
      uuid = db.query_commit(sql, {
        'handle': handle,
        'message': message,
        'expires_at': expires_at
      })
      return uuid
    def query_object_activity(uuid):
      sql = db.template('activities','object')
      return db.query_object_json(sql, {
        'uuid': uuid
      })
  ```
  - ### Update
  ```python
    #----------------Fetch Data from Postgres DB----------------
    sql = db.template('activities','home')
    results = db.query_array_json(sql)
    return results
  ```
  - ### Update Lambda
  ```python
  import os
import json
import psycopg2


def lambda_handler(event, context):
    user = event['request']['userAttributes']
    print('userAttributes')
    print(user)

    user_display_name  = user['name']
    user_email         = user['email']
    user_handle        = user['preferred_username']
    user_cognito_id    = user['sub']
    try:
      sql = f"""
         INSERT INTO public.users (
          display_name, 
          email,
          handle, 
          cognito_user_id
          ) 
        VALUES(%s,%s,%s,%s)
      """

      conn = psycopg2.connect(os.getenv('CONNECTION_URL'))
      cur = conn.cursor()
      params = [
        user_display_name,
        user_email,
        user_handle,
        user_cognito_id
      ]
      cur.execute(sql,(user_display_name, user_email, user_handle, user_cognito_id))
      conn.commit() 

    except (Exception, psycopg2.DatabaseError) as error:
      print(error)
    finally:
      if conn is not None:
          cur.close()
          conn.close()
          print('Database connection closed.')
    return event
  ```
  - ### Update the ActivityForm component in pages/HomeFeedPage.js to pass the user_handle prop.
  ```javascript
  <ActivityForm
    user_handle={user}
    popped={popped}
    setPopped={setPopped}
    setActivities={setActivities}
  />
  ```
  - ### In the components/ActivityForm.js component, update the fetch request body to include the user_handle

  ```javascript
  body: JSON.stringify({
  user_handle: props.user_handle.handle,
  message: message,
  ttl: ttl
}),
```
- ### In app.py, under the /api/activities route, assign the user_handle variable
```python
@app.route("/api/activities", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities():
  user_handle = request.json["user_handle"]
  ```
- ### Also update lambda as i was not able to post user data into rds
`function takes at most 2 arguments (5 given)`
```python
cur.execute(sql,(user_display_name, user_email, user_handle, user_cognito_id))
```