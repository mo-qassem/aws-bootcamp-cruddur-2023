# ------------- Start AWS-X Ray Global-Config -------------------
from aws_xray_sdk.core import xray_recorder
# ------------- End AWS-X Ray Global-Config -------------------
from datetime import datetime, timedelta, timezone
class NotificationsActivities:
  def run():
    # ------------- Start AWS-X Ray In App-code Config -------------------
    subsegment = xray_recorder.begin_subsegment('notifications_activities')
    # ------------- End AWS-X Ray In App-code Config ---------------------
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
    # ------------- Start AWS-X Ray In App-code Config -------------------
    dict = {
      'now': now.isoformat()
    }
    subsegment.put_metadata('key', dict, 'namespace')
    xray_recorder.end_subsegment()
    # ------------- End AWS-X Ray In App-code Config ---------------------
    return results