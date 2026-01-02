import requests
from google.transit import gtfs_realtime_pb2
from datetime import datetime, timezone

def check_nonzero_times():
    api_key = "28ebae1426ce43d2ae6e6c05cf7522a1"
    url = "https://api.nationaltransport.ie/gtfsr/v2/TripUpdates"
    headers = {"x-api-key": api_key}
    
    response = requests.get(url, headers=headers)
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    
    with_time = 0
    zero_time = 0
    
    for entity in feed.entity:
        if entity.HasField("trip_update"):
            for stu in entity.trip_update.stop_time_update:
                if stu.HasField("arrival") and stu.arrival.time > 0:
                    with_time += 1
                elif stu.HasField("arrival") and stu.arrival.time == 0:
                    zero_time += 1
                    
    print(f"Entities with absolute arrival time: {with_time}")
    print(f"Entities with zero arrival time: {zero_time}")

if __name__ == "__main__":
    check_nonzero_times()
