import requests
import sqlite3

def fetch_chargers_osm(
    # Following Longitude & Latitude apply to NI only
    lat_min=54.0,  # Bottom 
    lat_max=55.3,  # Top
    lon_min=-8.2,  # West
    lon_max=-5.3   # East
):
    print("Fetching data from OpenStreetMap...")

    overpass_url = "https://overpass-api.de/api/interpreter" # Overpass API endpoint URL for querying OpenStreetMap data


    # Get all nodes tagged as charging_station within the given bounding box, JSON output for easy parsing
    query = f"""
    [out:json];
    node["amenity"="charging_station"]({lat_min},{lon_min},{lat_max},{lon_max});
    out;
    """

    # GET req to Overpass API with constructed query
    response = requests.get(overpass_url, params={'data': query})
    response.raise_for_status() # error status codes 4xx or 5xx if unsuccessful GET req

    data = response.json()
    return data["elements"]

def store_chargers_osm(data):
    conn = sqlite3.connect("data/chargers.db")  # Connect to the local SQLite database file, if it doesn't exist it will be created
    cursor = conn.cursor()                      # NB: I use SQLite Viewer extension to view DB 

    # Counter 
    inserted = 0

    for item in data:
        charger_id = item["id"]
        title = item.get("tags", {}).get("name", "Unnamed Station")
        address = item.get("tags", {}).get("addr:street", "Unknown")
        lat = item.get("lat", 0)
        lon = item.get("lon", 0)
        is_free = 1 if item.get("tags", {}).get("fee", "no") == "no" else 0 # Check if charger is free to use based on 'fee' tag 
        power = None
        conn_type = None
        last_updated = None  # OSM doesn't track this per node

        # These above fields are left as None because OpenStreetMap (OSM) usually doesn't include this level of detail
        # For example, individual nodes (which represent single locations like charging stations) often don't have data about power output 
        # (in kW), connector type (e.g. Type 2, CCS), or when the information was last updated
        # These details depend on what contributors added,so we leave them blank to keep our database flexible and avoid errors

        # Insert the charger data into the database, 'INSERT OR IGNORE' prevents duplicates by ignoring records with an existing primary key
        # I created a cursor object above to be used here to ensure I can use SQL in Python
        cursor.execute("""
            INSERT OR IGNORE INTO chargers 
            (id, title, address, latitude, longitude, is_free, power_kw, connector_type, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (charger_id, title, address, lat, lon, is_free, power, conn_type, last_updated))

        inserted += 1

    conn.commit()
    conn.close()
    print(f"Inserted {inserted} OSM chargers into database.")

# This block runs when the script is executed directly (not imported as a module)
if __name__ == "__main__":
    data = fetch_chargers_osm()
    store_chargers_osm(data)