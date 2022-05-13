# Base file for taking interop data output and converting to QGC files. Files for the UGV and UAV are outputted.
import math
import json
from pyproj import Proj
import os


# Navigate to Mision File Directory and Load Mission from File
os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.chdir('..')
mission = open("interop_mission.txt", "r").read()
mission = json.loads(mission)

# Navigate Back to Directory for Outputted Files
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Set Variables
m2ft = 3.2808398950131235


def generate_UAV_plan():  # Create Plan/Mission for UAV
    # Setup Plan Dictionary
    plan = {
        "fileType": "Plan",
        "version": 1,
        "groundStation": "AAV Custom"
    }

    mission_items = []  # Create Mission Items List
    mission_items.append(TKOFF(30.48, "AGL"))  # Set Takeoff (ALT, ALT_TYPE)

    # Add Target Waypoints
    waypoints = mission["waypoints"]
    for waypoint in waypoints:
        # LAT, LONG, ALT, ALT_TYPE, DELAY
        waypoint_item = WP(
            waypoint['latitude'], waypoint['longitude'], waypoint['altitude']/m2ft, "MSL", 0)
        mission_items.append(waypoint_item)

    # Airdrop Information
    airdrop_lat = mission["airDropPos"]['latitude']
    airdrop_long = mission["airDropPos"]['longitude']
    airdrop_alt = 30.48  # Manually Enter Based On Testing (Relative Altitude)

    # Start Airdrop Sequence
    mission_items.append(WP(airdrop_lat, airdrop_long, airdrop_alt, "AGL", 5)) # Fly to Airdrop Location
    mission_items.append(SERVO(9, 1900))  # Trigger Release
    mission_items.append(SERVO(10, 1000))  # Trigger Winch (High Speed)
    mission_items.append(DELAY(10))  # High Speed Portion
    mission_items.append(SERVO(10, 1500))  # Trigger Winch (Low Speed w/ Stop)
    mission_items.append(DELAY(20))  # Wait for Delivery to Complete
    mission_items.append(SERVO(10, 1900))  # Real Back Winch
    mission_items.append(DELAY(15))  # Wait for Real Back to Complete
    mission_items.append(SERVO(10, 1500))  # Stop Winch
    # End Airdrop Sequence

    mission_items.append(RTL())  # RTL Command

    # Add Stationary Obstacles
    geoFence_circles = []
    obstacles = mission["stationaryObstacles"]
    for obstacle in obstacles:
        LAT, LONG = obstacle['latitude'], obstacle['longitude']
        RAD, ALT = obstacle['radius']/m2ft, obstacle['height']/m2ft
        geoFence_circle = ST_OBS(LAT, LONG, RAD, ALT)
        geoFence_circles.append(geoFence_circle)

    # Add Polygon Geofence
    geoFence_polygon = []
    boundaryPoints = mission["flyZones"][0]["boundaryPoints"]
    for boundaryPoint in boundaryPoints:
        LAT, LONG = boundaryPoint['latitude'], boundaryPoint['longitude']
        polygon_vertice = FENCE(LAT, LONG)
        geoFence_polygon.append(polygon_vertice)

    geoFence_polygon = [{"polygon": geoFence_polygon,
                         "inclusion": True,
                         "version": 1
                         }]

    # Add Information to Plan JSON
    plan["mission"] = {
        "cruiseSpeed": 1,
        "firmwareType": 3,
        "globalPlanAltitudeMode": 0,
        "hoverSpeed": 1,
        "items": mission_items,
        "plannedHomePosition": [38.145228, -76.426905, 0],
        "vehicleType": 2,
        "version": 2
    }

    plan["geoFence"] = {
        "version": 2,
        "circles": geoFence_circles,
        "polygons": geoFence_polygon
    }

    plan["rallyPoints"] = {
        "points": [],
        "version": 2
    }

    # Save Plan as .plan JSON File
    file = open("UAV_Mission.plan", "w+")
    file.write(json.dumps(plan))
    file.close()


def generate_UGV_plan():  # Create Plan/Mission for UGV
    # Setup Plan Dictionary
    plan = {
        "fileType": "Plan",
        "version": 1,
        "groundStation": "AAV Custom"
    }

    # Get Locations for Airdrop and UGV Drive Location
    airdrop_lat = mission["airDropPos"]['latitude']
    airdrop_long = mission["airDropPos"]['longitude']
    ugv_lat = mission["ugvDrivePos"]['latitude']
    ugv_long = mission["ugvDrivePos"]['longitude']

    # Create Mission to Drive to Location
    mission_items = []
    mission_items.append(SERVO(6, 2500)) # Release String via Servo Latch
    mission_items.append(DELAY(20)) # 20 Second Delay Before Starting Mission
    mission_items.append(WP(ugv_lat, ugv_long, 1, "AGL", 0))  # Set Target Location of UGV

    # Add Polygon Geofence
    geoFence_polygon = []
    boundaryPoints = mission["airDropBoundaryPoints"]
    for boundaryPoint in boundaryPoints:
        LAT, LONG = boundaryPoint['latitude'], boundaryPoint['longitude']
        polygon_vertice = FENCE(LAT, LONG)
        geoFence_polygon.append(polygon_vertice)

    geoFence_polygon = [{"polygon": geoFence_polygon,
                         "inclusion": True,
                         "version": 1
                         }]

    # Add Information to Plan JSON
    plan["mission"] = {
        "cruiseSpeed": 20,
        "firmwareType": 3,
        "globalPlanAltitudeMode": 0,
        "hoverSpeed": 20,
        "items": mission_items,
        "plannedHomePosition": [airdrop_lat, airdrop_long, 0],
        "vehicleType": 10,
        "version": 2
    }

    plan["geoFence"] = {
        "version": 2,
        "circles": [],
        "polygons": geoFence_polygon
    }

    plan["rallyPoints"] = {
        "points": [],
        "version": 2
    }

    # Save Plan as .plan JSON File
    file = open("UGV_Mission.plan", "w+")
    file.write(json.dumps(plan))
    file.close()


def generate_map():  # Create Mapping File
    map_height = mission["mapHeight"]/m2ft
    map_width = ((16.0/9.0)*map_height)
    map_cent_lat, map_cent_long = mission["mapCenterPos"]['latitude'], mission["mapCenterPos"]['longitude']

    # Convert Center UTM to Center XY
    utm_zone = math.floor((map_cent_long + 180)/6) + \
        1  # Calculate UTM Zone for Conversion
    # Setup Conversion Parameters
    utm_xy_conv = Proj(proj='utm', zone=utm_zone, ellps='WGS84')

    map_cent_x, map_cent_y = utm_xy_conv(map_cent_long, map_cent_lat)

    # Calculate Four Vertices in XY
    map_north_y, map_south_y = map_cent_y + map_height/2, map_cent_y - map_height/2
    map_east_x, map_west_x = map_cent_x + map_width/2, map_cent_x - map_width/2

    # Convert Four Vertise to UTM
    map_east_long, map_north_lat = utm_xy_conv(
        map_east_x, map_north_y, inverse=True)
    map_west_long, map_south_lat = utm_xy_conv(
        map_west_x, map_south_y, inverse=True)

    kml_start = ['<?xml version="1.0" encoding="UTF-8"?>',
                 '<kml xmlns="http://www.opengis.net/kml/2.2">',
                 '<Document><name>My document</name>',
                 '<description>Content</description>',
                 '<Style id="Lump">',
                 '<LineStyle><color>CD0000FF</color><width>2</width></LineStyle>',
                 '<PolyStyle><color>9AFF0000</color></PolyStyle>',
                 '</Style>',
                 '<Style id="Path">',
                 '<LineStyle><color>FF0000FF</color><width>3</width></LineStyle>',
                 '</Style>',
                 '<Style id="markerstyle">',
                 '<IconStyle><Icon><href>',
                 'http://maps.google.com/intl/en_us/mapfiles/ms/micons/red-dot.png',
                 '</href></Icon></IconStyle>',
                 '</Style>',
                 '<Placemark><name>NAME</name>',
                 '<description>YES</description>',
                 '<styleUrl>#Lump</styleUrl>',
                 '<Polygon>',
                 '<tessellate>1</tessellate>',
                 '<altitudeMode>clampToGround</altitudeMode>',
                 '<outerBoundaryIs><LinearRing><coordinates>']

    kml_end = ['</coordinates></LinearRing></outerBoundaryIs>',
               '</Polygon>',
               '</Placemark>',
               '</Document>',
               '</kml>']

    map_point = []
    map_point.append(str(map_east_long) + "," + str(map_north_lat) + ",0.0")
    map_point.append(str(map_west_long) + "," + str(map_north_lat) + ",0.0")
    map_point.append(str(map_west_long) + "," + str(map_south_lat) + ",0.0")
    map_point.append(str(map_east_long) + "," + str(map_south_lat) + ",0.0")
    map_point.append(str(map_east_long) + "," + str(map_north_lat) + ",0.0")

    # Create KML File
    file = open("mapping.kml", "w+")

    kml = kml_start + map_point + kml_end
    for entry in kml:
        file.write(entry + "\n")

    file.close()


def generate_search():  # Create Search Area File
    kml_start = ['<?xml version="1.0" encoding="UTF-8"?>',
                 '<kml xmlns="http://www.opengis.net/kml/2.2">',
                 '<Document><name>My document</name>',
                 '<description>Content</description>',
                 '<Style id="Lump">',
                 '<LineStyle><color>CD0000FF</color><width>2</width></LineStyle>',
                 '<PolyStyle><color>9AFF0000</color></PolyStyle>',
                 '</Style>',
                 '<Style id="Path">',
                 '<LineStyle><color>FF0000FF</color><width>3</width></LineStyle>',
                 '</Style>',
                 '<Style id="markerstyle">',
                 '<IconStyle><Icon><href>',
                 'http://maps.google.com/intl/en_us/mapfiles/ms/micons/red-dot.png',
                 '</href></Icon></IconStyle>',
                 '</Style>',
                 '<Placemark><name>NAME</name>',
                 '<description>YES</description>',
                 '<styleUrl>#Lump</styleUrl>',
                 '<Polygon>',
                 '<tessellate>1</tessellate>',
                 '<altitudeMode>clampToGround</altitudeMode>',
                 '<outerBoundaryIs><LinearRing><coordinates>']

    kml_end = ['</coordinates></LinearRing></outerBoundaryIs>',
               '</Polygon>',
               '</Placemark>',
               '</Document>',
               '</kml>']

    search_vertices = []
    boundaries = mission["searchGridPoints"]
    for boundary in boundaries:
        LAT, LONG = boundary['latitude'], boundary['longitude']
        search_vertices.append(str(LONG) + "," + str(LAT) + ",0.0")

    # Close Loop By Adding Firs Point to End
    search_vertices.append(search_vertices[0])

    # Create KML File
    file = open("searcharea.kml", "w+")

    kml = kml_start + search_vertices + kml_end
    for entry in kml:
        file.write(entry + "\n")

    file.close()


def WP(LAT, LONG, ALT, ALT_TYPE, DELAY):  # Convert WP to Mission WP
    P1 = DELAY  # Hover at WP for Delay
    P2 = 0  # No Effect
    P3 = 0  # No Effect
    P4 = 0  # No Effect
    P5 = LAT  # Latitude Location
    P6 = LONG  # Longitude Location
    P7 = ALT  # Altitude (m)
    
    if ALT_TYPE == "MSL":
        alt_mode = 2
        frame = 0
    elif ALT_TYPE == "AGL":
        alt_mode = 1
        frame = 3

    waypoint_item = {
        "AMSLAltAboveTerrain": 0,
        "Altitude": ALT,
        "AltitudeMode": alt_mode,
        "autoContinue": True,
        "command": 16,  # WP Command is 16
        "doJumpId": 1,
        "frame": frame,
        "params": [P1, P2, P3, P4, P5, P6, P7],
        "type": "SimpleItem"
    }

    return waypoint_item


def TKOFF(ALT, ALT_TYPE):  # TKOFF Mission Item Generation
    P1 = 0  # No Effect
    P2 = 0  # No Effect
    P3 = 0  # No Effect
    P4 = 0  # No Effect
    P5 = 0  # No Effect
    P6 = 0  # No Effect
    P7 = ALT  # Altitude (m)

    if ALT_TYPE == "MSL":
        alt_mode = 2
        frame = 0
    elif ALT_TYPE == "AGL":
        alt_mode = 1
        frame = 3

    takeoff_item = {
        "AMSLAltAboveTerrain": 0,
        "Altitude": ALT,
        "AltitudeMode": alt_mode,
        "autoContinue": True,
        "command": 22,  # Takeoff Command is 22
        "doJumpId": 1,
        "frame": frame,
        "params": [P1, P2, P3, P4, P5, P6, P7],
        "type": "SimpleItem"
    }

    return takeoff_item


def RTL():  # RTL Mission Item Generation
    P1 = 0  # No Effect
    P2 = 0  # No Effect
    P3 = 0  # No Effect
    P4 = 0  # No Effect
    P5 = 0  # No Effect
    P6 = 0  # No Effect
    P7 = 0  # No Effect

    rtl_item = {
        "autoContinue": True,
        "command": 20,  # RTL Command is 20
        "doJumpId": 1,
        "frame": 2,
        "params": [P1, P2, P3, P4, P5, P6, P7],
        "type": "SimpleItem"
    }

    return rtl_item


def SERVO(SERVO_NUM, PWM):  # SERVO Mission Item Generation
    P1 = SERVO_NUM  # Servo Number
    P2 = PWM  # PWM Out
    P3 = 0  # No Effect
    P4 = 0  # No Effect
    P5 = 0  # No Effect
    P6 = 0  # No Effect
    P7 = 0  # No Effect

    servo_item = {
        "autoContinue": True,
        "command": 183,  # Servo Command is 183
        "doJumpId": 1,
        "frame": 2,
        "params": [P1, P2, P3, P4, P5, P6, P7],
        "type": "SimpleItem"
    }

    return servo_item

def DELAY(TIME):  # Delay Mission Item Generation
    P1 = TIME  # Delay Time (sec)
    P2 = 0  # No Effect
    P3 = 0  # No Effect
    P4 = 0  # No Effect
    P5 = 0  # No Effect
    P6 = 0  # No Effect
    P7 = 0  # No Effect

    delay_item = {
        "autoContinue": True,
        "command": 93,  # Delay Command is 93
        "doJumpId": 1,
        "frame": 2,
        "params": [P1, P2, P3, P4, P5, P6, P7],
        "type": "SimpleItem"
    }

    return delay_item


def ST_OBS(LAT, LONG, RAD, ALT):  # Convert ST_OBS to Circular Exclusion Fences
    geoFence_circle = {}
    geoFence_circle["circle"] = {}
    geoFence_circle["circle"]["center"] = [LAT, LONG]
    geoFence_circle["circle"]["radius"] = RAD + ALT/1000
    geoFence_circle["inclusion"] = False
    geoFence_circle["version"] = 1

    return geoFence_circle


def FENCE(LAT, LONG):  # Converted Polygon Vertices to Polygon Fence Verticies
    polygon_vertice = [LAT, LONG]

    return polygon_vertice


if __name__ == "__main__":
    generate_UAV_plan()  # Generate File for UAV Mission
    generate_UGV_plan()  # Generate File for UGV Mission
    generate_map()  # Generate File for Mapping
    generate_search()  # Generate File for Search Area
