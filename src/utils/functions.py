from datetime import datetime, timedelta


def get_current_timestamp():
    return datetime.now().isoformat()

def format_time(time_str):
    try:
        if 'ago' in time_str:
            time_str = time_str.replace(' ago', '')

            if 'minute' in time_str:
                minutes = int(time_str.replace(' minutes', '').replace(' minute', ''))
                dt = datetime.now() - timedelta(minutes=minutes)
            elif 'hour' in time_str:
                hours = int(time_str.replace(' hours', '').replace(' hour', ''))
                dt = datetime.now() - timedelta(hours=hours)
            elif 'day' in time_str:
                days = int(time_str.replace(' days', '').replace(' day', ''))
                dt = datetime.now() - timedelta(days=days)
            else:
                return None

            return dt.isoformat()

        return None
    except ValueError:
        return None