import requests
from google.transit import gtfs_realtime_pb2
from datetime import datetime, timezone

def debug_1192():
    api_key = "28ebae1426ce43d2ae6e6c05cf7522a1"
    url = "https://api.nationaltransport.ie/gtfsr/v2/TripUpdates"
    headers = {"x-api-key": api_key}
    
    response = requests.get(url, headers=headers)
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    
    now = datetime.now(timezone.utc).timestamp()
    print(f"Current Timestamp: {now}")
    
    matches = 0
    for entity in feed.entity:
        if entity.HasField("trip_update"):
            for stu in entity.trip_update.stop_time_update:
                if "1192" in stu.stop_id:
                    matches += 1
                    print(f"\nMatch {matches}: Stop {stu.stop_id}")
                    print(f"  Trip: {entity.trip_update.trip.trip_id}")
                    print(f"  Route: {entity.trip_update.trip.route_id}")
                    
                    arr = stu.arrival
                    dep = stu.departure
                    
                    print(f"  Arrival Time: {arr.time if stu.HasField('arrival') else 'MISSING'}")
                    print(f"  Arrival Delay: {arr.delay if stu.HasField('arrival') else 'MISSING'}")
                    print(f"  Departure Time: {dep.time if stu.HasField('departure') else 'MISSING'}")
                    
                    if stu.HasField('arrival') and arr.time > 0:
                        diff = (arr.time - now) / 60
                        print(f"  Minutes away: {diff:.1f}")

    if matches == 0:
        print("No matches for 1192 found.")

if __name__ == "__main__":
    debug_1192()
