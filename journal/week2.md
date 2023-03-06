# Week 2 — Distributed Tracing

### Homework Tasks

| TASKs                                               | COMPLETED          |
| --------------------------------------------------- | ------------------ |
| Instrument Honeycomb with OTEL.                     | :heavy_check_mark: |
| Instrument AWS X-Ray.                               | :heavy_check_mark: |
| Configure custom logger to send to CloudWatch Logs. | :heavy_check_mark: |
| Integrate Rollbar and capture and error.            | :heavy_check_mark: |

---

## 1. Instrument Honeycomb with OTEL.

- ### Add required Python libraries to `requirements.txt`.

  ```shell
  opentelemetry-api
  opentelemetry-sdk
  opentelemetry-exporter-otlp-proto-http
  opentelemetry-instrumentation-flask
  opentelemetry-instrumentation-requests
  ```

- ### Install them by running

  ```shell
  pip install -r requirements.txt
  ```

- ### Update `app.py` with below code.

  ```python
  #--------------Honeycomb Global-Config-------------------
  from opentelemetry import trace
  from opentelemetry.instrumentation.flask import FlaskInstrumentor
  from opentelemetry.instrumentation.requests import RequestsInstrumentor
  from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
  from opentelemetry.sdk.trace import TracerProvider
  from opentelemetry.sdk.trace.export import BatchSpanProcessor
  #--Show Logs in STOUT-Testing
  from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
  #--------Initialize tracing and an exporter that can send data to Honeycomb------
  provider = TracerProvider()
  processor = BatchSpanProcessor(OTLPSpanExporter())
  provider.add_span_processor(processor)

  #--Show Logs in STOUT-Testing
  simple_processor = SimpleSpanProcessor(ConsoleSpanExporter())
  provider.add_span_processor(simple_processor)

  trace.set_tracer_provider(provider)
  tracer = trace.get_tracer(__name__)
  ```

- ### Add below `app = Flask(__name__)`

  ```python
  #--------------Honeycomb IN-LINE Config------------------
  FlaskInstrumentor().instrument_app(app)
  RequestsInstrumentor().instrument()
  ```

- ### Add environment variables for `cruddur-backend-flask` in `docker-compose.yaml`

  ```yaml
  OTEL_EXPORTER_OTLP_ENDPOINT: "https://api.honeycomb.io"
  OTEL_EXPORTER_OTLP_HEADERS: "x-honeycomb-team=${HONEYCOMB_API_KEY}"
  OTEL_SERVICE_NAME: "${HONEYCOMB_SERVICE_NAME}"
  ```

- ### Export `Honeycomb` API key and service name.

  ```shell
  export HONEYCOMB_API_KEY=""
  gp env HONEYCOMB_API_KEY=""
  export HONEYCOMB_SERVICE_NAME="Cruddur"
  gp env HONEYCOMB_SERVICE_NAME="Cruddur"
  ```

- ### Create a custom Span for `home_activities.py`
  ```python
  #--------------Honeycomb Global-Config-------------------
  from opentelemetry import trace
  tracer = trace.get_tracer("home.activities")
  ```
- ### Update `run` funcation to set attribute for the custom span.
  ```python
  def run(Logger):
      #--------------Honeycomb IN-LINE Config-------------------
      with tracer.start_as_current_span("HomeActivities-MockData"):
      span = trace.get_current_span()
      now = datetime.now(timezone.utc).astimezone()
      span.set_attribute("home-activities-app.now", now.isoformat())
  ```
  ```python
  #--------------Honeycomb IN-LINE Config-------------------
  span.set_attribute("home-activities-app.result_length", len(results))
  return results
  ```
  ![honeycomb](/journal/screenshots/week2_honeycomb.png)

## 2. Instrument AWS X-Ray.

- ### Export environment variables.

  ```shell
  export AWS_REGION="us-east-1"
  gp env AWS_REGION="us-east-1"
  ```

- ### Update `requirements.txt` to add.

  ```shell
  aws-xray-sdk
  ```

- ### Install it by run.

  ```shell
  pip3 install -r requirements.txt
  ```

- ### Create trace group using `AWS-CLI` under name `Backend-Flask`

  ```shell
  aws xray create-group \
  --group-name "Cruddur" \
  --filter-expression "service(\"Backend-Flask\")"
  ```

- ### Create `Sampling` rule to configure which requests to record `AWS-CLI`.

  ```shell
  aws xray create-sampling-rule --cli-input-json file://aws/json/xray.json
  ```

- ### Update `app.py` with required code for X-Ray.

  ```python
  # -------------AWS-X Ray Global-Config-------------------
  from aws_xray_sdk.core import xray_recorder
  from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
  xray_url = os.getenv("AWS_XRAY_URL")
  ```

  ```python
  # -------------AWS-X Ray IN-LINE Config-------------------
  xray_recorder.configure(service='Backend-Flask', dynamic_naming=xray_url)
  XRayMiddleware(app, xray_recorder)
  ```

- ### Update `docker-compose.yaml` to add X-Ray Deamon as container service.

  ```yaml
  xray-daemon:
  image: "amazon/aws-xray-daemon"
  environment:
  AWS_ACCESS_KEY_ID: "${AWS_ACCESS_KEY_ID}"
  AWS_SECRET_ACCESS_KEY: "${AWS_SECRET_ACCESS_KEY}"
  AWS_REGION: "${AWS_REGION}"
  command:
    - "xray -o -b xray-daemon:2000"
  ports:
    - 2000:2000/udp
  ```

- ### Add to `docker-compose.yaml` under `cruddur-backend-flask` below environment variables.

  ```yaml
  AWS_XRAY_URL: "*4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}*"
  AWS_XRAY_DAEMON_ADDRESS: "xray-daemon:2000"
  ```

- ### Update `notifications_activities.py` to add subsgemnt to be catch by X-Ray.

  ```python
  # -------------AWS-X Ray Global-Config-------------------
  from aws_xray_sdk.core import xray_recorder
  ```

  ```python
  # -------------AWS-X Ray IN-LINE Config-------------------
  subsegment = xray_recorder.begin_subsegment('notifications_activities')

  dict = {
      'now': now.isoformat(),
      'results-size': results[0].values()
      }
  subsegment.put_metadata('key', dict, 'namespace')
  xray_recorder.end_subsegment()
  ```

  ![x-ray](/journal/screenshots/week2_notifications_activities2.png)

  ![x-ray](/journal/screenshots/week2_notifications_activities.png)

## 3. Configure custom logger to send to CloudWatch Logs.

- ### Update `requirements.txt` to add and install below library.

  ```shell
  watchtower
  ```

- ### Update `app.py` with required code CloudWatch Logs.

  ```python
  # -------------CloudWatch Global-Config-------------------
  import watchtower
  import logging
  from time import strftime
  #------------Configuring Logger to Use CloudWatch-------
  LOGGER = logging.getLogger(__name__)
  LOGGER.setLevel(logging.DEBUG)
  console_handler = logging.StreamHandler()
  cw_handler = watchtower.CloudWatchLogHandler(log_group='Cruddur-Backend-Flask')
  LOGGER.addHandler(console_handler)
  LOGGER.addHandler(cw_handler)
  ```

  ```python
  # -------------CloudWatch IN-LINE Config-------------------
  @app.after_request
  def after_request(response):
      timestamp = strftime('[%Y-%b-%d %H:%M]')
      LOGGER.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
      return response
  ```

- ### Update logger configs for notifications api in `app.py`

  ```python
  @app.route("/api/activities/notifications", methods=['GET'])
  def data_notifications():
  # -------------CloudWatch IN-LINE Config-------------------
  data = NotificationsActivities.run(Logger=LOGGER)
  return data, 200
  ```

- ### Add logger configuration in `notifications_activities.py`

  ```python
  # -------------CloudWatch IN-LINE Config-------------------
  class NotificationsActivities:
  def run(Logger):
      Logger.info('Hello CloudWatch! from  /api/activities/notifications')
  ```

- ### Upate env-vars for `cruddur-backend-flask` in `docker-compose.yml`

  ```shell
  AWS_DEFAULT_REGION: "${AWS_DEFAULT_REGION}"
  AWS_ACCESS_KEY_ID: "${AWS_ACCESS_KEY_ID}"
  AWS_SECRET_ACCESS_KEY: "${AWS_SECRET_ACCESS_KEY}"
  ```

  ![cloudwatch](/journal/screenshots/week2_cloudwatchlogs.png)
  ![cloudwatch](/journal/screenshots/week2_cloudwatchlogs2.png)
  ![cloudwatch](/journal/screenshots/week2_cloudwatchlogs3.png)

## 4. Integrate Rollbar and capture and error.

- ### Export env-vars

  ```shell
  export ROLLBAR_ACCESS_TOKEN=""
  gp env ROLLBAR_ACCESS_TOKEN=""
  ```

- ### Add and install below libraries to `requirements.txt`

  ```shell
  blinker
  rollbar
  ```

- ### Update `app.py` with below code to configure Rollbar.

  ```python
  # -------------Rollbar Global-Config------------------
  import rollbar
  import rollbar.contrib.flask
  from flask import got_request_exception
  ```

  ```python
  rollbar_access_token = os.getenv('ROLLBAR_ACCESS_TOKEN')
  @app.before_first_request
  def init_rollbar():
      """init rollbar module"""
      rollbar.init(
          # access token
          rollbar_access_token,
          # environment name
          'production',
          # server root directory, makes tracebacks prettier
          root=os.path.dirname(os.path.realpath(__file__)),
          # flask already sets up logging
          allow_logging_basic_config=False)

      # send exceptions from `app` to rollbar, using flask's signal system.
      got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

  @app.route('/rollbar/test')
  def rollbar_test():
      rollbar.report_message('Hello World!', 'warning')
      return "Hello World!"
  ```

- ### Update env-vars `cruddur-backend-flask` in `docker-compose.yaml`

  ```shell
  ROLLBAR_ACCESS_TOKEN: "${ROLLBAR_ACCESS_TOKEN}"
  ```

## ![rollbar](/journal/screenshots/week2_rollbar.png)

### Homework Challenges

| TASKs                                                                                                            | COMPLETED                |
| ---------------------------------------------------------------------------------------------------------------- | ------------------------ |
| Instrument Honeycomb for the frontend-application to observe network latency between frontend and backend[HARD]. | :heavy_exclamation_mark: |
| Add custom instrumentation to Honeycomb to add more attributes eg. UserId, Add a custom span.                    | :heavy_exclamation_mark: |
| Run custom queries in Honeycomb and save them later eg. Latency by UserID, Recent Traces.                        | :heavy_exclamation_mark: |

---

- ### Instrument Honeycomb for the frontend-application to observe network latency between frontend and backend.
