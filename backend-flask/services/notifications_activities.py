# -------------AWS-X Ray Global-Config-------------------
from aws_xray_sdk.core import xray_recorder
# ---------------------------------------------------------

from datetime import datetime, timedelta, timezone
class NotificationsActivities:
    # -------------CloudWatch IN-LINE Config-------------------
  def run(Logger):
    Logger.info('Hello CloudWatch! from  /api/activities/notifications')
    # ---------------------------------------------------------


    # -------------AWS-X Ray IN-LINE Config-------------------
    subsegment = xray_recorder.begin_subsegment('notifications_activities')
    # ---------------------------------------------------------

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
    # -------------AWS-X Ray IN-LINE Config-------------------
    dict = {
      'now': now.isoformat(),
      'results-size': results[0].values()
    }
    subsegment.put_metadata('key', dict, 'namespace')
    xray_recorder.end_subsegment()
    # ---------------------------------------------------------
    return results