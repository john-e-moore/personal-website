from datetime import datetime

def compute_time_diff(timestamp):
    post_date = datetime.strptime(timestamp, '%Y%m%d')
    diff = datetime.now() - post_date
    days = diff.days
    if days < 1:
        return 'today'
    elif days == 1:
        return 'yesterday'
    else:
        return f'{days} days ago'