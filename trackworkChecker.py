import requests
from pytz import timezone
import config
from datetime import datetime, timedelta

# Check if its occuring within next 4 and 5 days and on weekend
def correctDates(date):
    now = datetime.now(timezone('Australia/Sydney'))
    next_4_days = now + timedelta(days=4)
    next_5_days = now + timedelta(days=5)
    return (next_4_days <= date < next_5_days) and date.weekday() >=4

# Check if alerts refer to trackwork service
def correctAlerts(entry):
    return entry['alert']['cause'] == 'MAINTENANCE' and entry['alert']['effect'] == 'MODIFIED_SERVICE'

# Check if trackwork is for North Shore Line (Cause we all live on it)
def includesRelatedLines(entry):
    for trainLine in entry['informedEntity']:
        if trainLine['routeId'][0:3] == 'NSN':
            filterText = "T1 North Shore Line:"
            if filterText in entry['headerText']['translation'][0]['text']:
                return True
    return False

def noTrackWork(output):
    return True if 'entity' not in output else False

def getNewTrackWork():
    api_url = "https://api.transport.nsw.gov.au/v2/gtfs/alerts/sydneytrains?format=json"
    response = requests.get(api_url, headers={'Authorization': f'apikey {config.api_key}'})
    output = response.json()
    if noTrackWork(output):
        return None
    for entry in output['entity']:
        startTime = int(entry['alert']['activePeriod'][0]['start'])
        dateTime = datetime.fromtimestamp(startTime, timezone('Australia/Sydney'))
        if (correctDates(dateTime) and correctAlerts(entry) and includesRelatedLines(entry['alert'])):
            # Return the trackwork message
            return entry['alert']['descriptionText']['translation'][0]['text']
    return None

def getNewMetroTrackWork():
    api_url = "https://api.transport.nsw.gov.au/v2/gtfs/alerts/metro?format=json"
    response = requests.get(api_url, headers={'Authorization': f'apikey {config.api_key}'})
    output = response.json()
    # Check if there's any trackwork at all
    if noTrackWork(output):
        return None
    for entry in output['entity']:
        startTime = int(entry['alert']['activePeriod'][0]['start'])
        dateTime = datetime.fromtimestamp(startTime, timezone('Australia/Sydney'))
        if (correctDates(dateTime) and correctAlerts(entry)):
            # Return the trackwork message
            return entry['alert']['descriptionText']['translation'][0]['text']
    return None

if __name__ == "__main__":
    getNewMetroTrackWork()
