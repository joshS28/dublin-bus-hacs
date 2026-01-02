import requests
from google.transit import gtfs_realtime_pb2
import sys

def debug_nta():
    api_key = "28ebae1426ce43d2ae6e6c05cf7522a1"
    url = "https://api.nationaltransport.ie/gtfsr/v2/TripUpdates"
    
    headers = {
        "x-api-key": api_key,
        "Cache-Control": "no-cache",
    }
    
    print(f"Fetching from {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        print(f"Status: {response.status_code}")
        print(f"Content Length: {len(response.content)}")
        
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        
        print(f"Header timestamp: {feed.header.timestamp}")
        print(f"Total entities: {len(feed.entity)}")
        
        # Check first 5 entities
        for i, entity in enumerate(feed.entity[:5]):
            if entity.HasField("trip_update"):
                tu = entity.trip_update
                print(f"\nEntity {i}: Trip {tu.trip.trip_id}, Route {tu.trip.route_id}")
                for stu in tu.stop_time_update[:3]:
                    print(f"  Stop: {stu.stop_id}, Arrival: {stu.arrival.time if stu.HasField('arrival') else 'N/A'}")
                    
        # Look specifically for stop 1192 symbols
        print("\nSearching for stop 1192 related IDs...")
        found = 0
        for entity in feed.entity:
            if entity.HasField("trip_update"):
                for stu in entity.trip_update.stop_time_update:
                    if "1192" in stu.stop_id:
                        print(f"Found match: Stop ID in feed: {stu.stop_id}")
                        found += 1
                        if found > 5: break
            if found > 5: break
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_nta()
