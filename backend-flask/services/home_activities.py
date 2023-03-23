# -------------AWS-X Ray Global-Config-------------------
from aws_xray_sdk.core import xray_recorder
# -------------------------------------------------------

#--------------Honeycomb Global-Config-------------------
from opentelemetry import trace
tracer = trace.get_tracer("home.activities")
#--------------------------------------------------------

#---------COnfigure postgres pool-----------------
from lib.db import db
#--------------------------------------------------

from datetime import datetime, timedelta, timezone
class HomeActivities:
  def run(Logger, cognito_user_id=None):

    #--------------Honeycomb IN-LINE Config-------------------
    with tracer.start_as_current_span("HomeActivities-MockData"): 
      span = trace.get_current_span()
      now = datetime.now(timezone.utc).astimezone()
      span.set_attribute("home-activities-app.now", now.isoformat())
    #----------------------------------------------------------

    # -------------CloudWatch IN-LINE Config------------------- 
      Logger.info('Hello CloudWatch! from  /api/activities/home')
    # ---------------------------------------------------------

    # -------------AWS-X Ray IN-LINE Config-------------------
    subsegment = xray_recorder.begin_subsegment('home_activities')
  # --------------------------------------------------------------
  
  #----------------Fetch Data from Postgres DB----------------
    sql = db.template('activities','home')
    results = db.query_array_json(sql)
    return results
        
    # -------------AWS-X Ray IN-LINE Config-------------------
    # dict = {
    #   'now': now.isoformat()
    # }
    # subsegment.put_metadata('key', dict, 'namespace')
    # xray_recorder.end_subsegment()
    # -------Extra Crud if Your Authenticated--------------------
    # if cognito_user_id != None:
    #         extra_crud = {
    #           'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
    #           'handle':  'Dwight Schrute',
    #           'message': 'Always The Padawan, Never The Jedi!',
    #           'created_at': (now - timedelta(hours=1)).isoformat(),
    #           'expires_at': (now + timedelta(hours=12)).isoformat(),
    #           'likes': 10,
    #           'replies': []
    #         }
    #         results.insert(0, extra_crud)
    #--------------Honeycomb IN-LINE Config-------------------
    span.set_attribute("home-activities-app.result_length", len(results))
    #----------------------------------------------------------
    