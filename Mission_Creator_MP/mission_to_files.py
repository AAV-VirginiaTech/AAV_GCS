# THIS FILE HAS NOT BEEN UPDATED/TOUCHED SINCE THE TEAM MOVED TO QGroundControl in Spring 2022! THUS - SOME FEATURES MAY BE MISSING!

# Base file for taking interop data output and converting to mission planner files. Multiple files for the UGV and UAV are outputted.
import math
import json
from pyproj import Proj
import os


# Navigate to Mision File Directory and Load Mission from File
os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.chdir('..')
mission = open("interop_mission.txt", "r").read()
mission = json.loads(mission)
template = '{0:d}\t{1:d}\t{2:d}\t{3:d}\t{4:.8f}\t{5:.8f}\t{6:.8f}\t{7:.8f}\t{8:.8f}\t{9:.8f}\t{10:.8f}\t{11:d}\n'

# Navigate Back to Directory for Outputted Files
os.chdir(os.path.dirname(os.path.realpath(__file__)))


# ------------------------------------------------------------------------------------------------------------------

def WP(LAT, LONG, ALT, ALT_TYPE, DELAY): # Function for WP Command Line Generation
    ROW = 0 # Row Numbering Does Not Matter
    CURRENT = False # Current = False for All Except Home
    ALT_TYPE = ALT_TYPE # 0 is MSL, 3 is AGL
    CMD = 16 # WP Command is 16
    P1 = DELAY # Hover at WP for Delay
    P2 = 0 # No Effect
    P3 = 0 # No Effect
    P4 = 0 # No Effect
    P5 = LAT # Latitude Location
    P6 = LONG # Longitude Location
    P7 = ALT # Altitude (m)
    AUTOCONTINUE = True # Continue With Auto Mission
    
    WP.Line = template.format(ROW, CURRENT, ALT_TYPE, CMD, P1, P2, P3, P4, P5, P6, P7, AUTOCONTINUE)
    file.write(WP.Line)
    
def HOME(LAT, LONG): # Function for Home Command Line Generation
    ROW = 0 # Row Numbering Does Not Matter
    CURRENT = True # Current = False for All Except Home
    ALT_TYPE = 0 # 0 is MSL, 3 is AGL
    CMD = 16 # Home Command is 16
    P1 = 0 # No Effect
    P2 = 0 # No Effect
    P3 = 0 # No Effect
    P4 = 0 # No Effect
    P5 = LAT # Latitude Location
    P6 = LONG # Longitude Location
    P7 = 0 # Altitude (m)
    AUTOCONTINUE = True # Continue With Auto Mission
    
    HOME.Line = template.format(ROW, CURRENT, ALT_TYPE, CMD, P1, P2, P3, P4, P5, P6, P7, AUTOCONTINUE)
    file.write(HOME.Line)

def TKOFF(ALT): # Function for TKOFF Command Line Generation
    ROW = 0 # Row Numbering Does Not Matter
    CURRENT = False # Current = False for All Except Home
    ALT_TYPE = 0 # 0 is MSL, 3 is AGL
    CMD = 22 # Takeoff Command is 22
    P1 = 0 # No Effect
    P2 = 0 # No Effect
    P3 = 0 # No Effect
    P4 = 0 # No Effect
    P5 = 0 # No Effect
    P6 = 0 # No Effect
    P7 = ALT # Altitude (m)
    AUTOCONTINUE = True # Continue With Auto Mission
    
    TKOFF.Line = template.format(ROW, CURRENT, ALT_TYPE, CMD, P1, P2, P3, P4, P5, P6, P7, AUTOCONTINUE)
    file.write(TKOFF.Line)
    
def SERVO(SERVO_NUM, PWM): # Function for SERVO Command Line Generation
    ROW = 0 # Row Numbering Does Not Matter
    CURRENT = False # Current = False for All Except Home
    ALT_TYPE = 3 # No Effect
    CMD = 183 # Servo Trigger Command is 183
    P1 = SERVO_NUM # Servo Number
    P2 = PWM # PWM Out
    P3 = 0 # No Effect
    P4 = 0 # No Effect
    P5 = 0 # No Effect
    P6 = 0 # No Effect
    P7 = 0 # Not Effect
    AUTOCONTINUE = True # Continue With Auto Mission
    
    SERVO.Line = template.format(ROW, CURRENT, ALT_TYPE, CMD, P1, P2, P3, P4, P5, P6, P7, AUTOCONTINUE)
    file.write(SERVO.Line)
    
def POLYGON(LAT, LONG): # Function for Polygon Line Generation
    POLYGON.Line = str(LAT) + ' ' + str(LONG) + '\n'
    file.write(POLYGON.Line)
    
def ST_OBS(LAT, LONG, RAD, ALT): # Function for ST_OBS Line Generation
    ROW = 0 # Row Numbering Does Not Matter
    CURRENT = False # Current = False for All Except Home
    ALT_TYPE = 0 # 0 is MSL, 3 is AGL
    CMD = 5004 # Circular Exlusion is 5004
    P1 = RAD # Cylinder Radius
    P2 = 0 # No Effect
    P3 = 0 # No Effect
    P4 = 0 # No Effect
    P5 = LAT # Latitude Location
    P6 = LONG # Longitude Location
    P7 = ALT # Altitude (m)
    AUTOCONTINUE = True # Continue With Auto Mission
    
    ST_OBS.Line = template.format(ROW, CURRENT, ALT_TYPE, CMD, P1, P2, P3, P4, P5, P6, P7, AUTOCONTINUE)
    file.write(ST_OBS.Line)

def FENCE(LAT, LONG, ALT, NUM_POINTS): # Function for FENCE Line Generation
    ROW = 0 # Row Numbering Does Not Matter
    CURRENT = False # Current = False for All Except Home
    ALT_TYPE = 0 # 0 is MSL, 3 is AGL
    CMD = 5001 # Fence Inclusion is 5001
    P1 = NUM_POINTS # Number of Sides
    P2 = 0 # No Effect
    P3 = 0 # No Effect
    P4 = 0 # No Effect
    P5 = LAT # Latitude Location
    P6 = LONG # Longitude Location
    P7 = ALT # Altitude (m)
    AUTOCONTINUE = True # Continue With Auto Mission
    
    FENCE.Line = template.format(ROW, CURRENT, ALT_TYPE, CMD, P1, P2, P3, P4, P5, P6, P7, AUTOCONTINUE)
    file.write(FENCE.Line)

# ------------------------------------------------------------------------------------------------------------------
    
# UAV Mission File (Waypoints + Airdrop)
file = open("UAV_mission.waypoints",'w+')
file.write("QGC WPL 110\n")  # Required Header for Waypoint Files

HOME(38.145228, -76.426905) # Set Home Point (LAT, LONG)
TKOFF(30.48) # Set Takeoff (ALT, ALT_TYPE)

# Addition of Target Waypoints
waypoints = mission["waypoints"]
for waypoint in waypoints:
    WP(waypoint['latitude'], waypoint['longitude'], waypoint['altitude']/3.28084, 0, 0) # LAT, LONG, ALT, ALT_TYPE, DELAY

# Addition of Airdrop Sequence (Relative Altitudes)
airdrop_lat = mission["airDropPos"]['latitude']
airdrop_long = mission["airDropPos"]['longitude']
airdrop_alt = 30.48 # Manually Enter Based On Testing

WP(airdrop_lat, airdrop_long, airdrop_alt, 3, 0) # Fly to Airdrop Location
SERVO(11, 1900) # Trigger Release
SERVO(10, 900) # Trigger Winch
WP(airdrop_lat, airdrop_long, airdrop_alt, 3, 20) # Wait for Delivery
SERVO(10, 2100) # Real Back Winch
WP(airdrop_lat, airdrop_long, airdrop_alt, 3, 20) # Wait for Real Back
SERVO(10, 1500) # Stop Winch

file.close() # Close File

# ------------------------------------------------------------------------------------------------------------------

# UGV Mission File
file = open("UGV_mission.waypoints", "w+")
file.write("QGC WPL 110\n")  # Required Header for Waypoint Files

ugv_lat = mission["ugvDrivePos"]['latitude']
ugv_long = mission["ugvDrivePos"]['longitude']

HOME(airdrop_lat, airdrop_long) # Set Home Location of UGV
WP(ugv_lat, ugv_long, 0, 0, 0) # Set Target Location of UGV

file.close() #Close File

# ------------------------------------------------------------------------------------------------------------------

#UAV Fence File (Obstacles + Geofence)
file = open("UAV_fence.waypoints",'w+') 
file.write("QGC WPL 110\n") # Required Header for Waypoint Files

HOME(38.145228, -76.426905) # Set Home Point (LAT, LONG)

# Add Obstacles to Fence File
obstacles = mission["stationaryObstacles"]
for obstacle in obstacles:
    ST_OBS(obstacle['latitude'], obstacle['longitude'], obstacle['radius']/3.28084, obstacle['height']/3.28084) 
  
# Add Geofence to Fence File
boundaryPoints = mission["flyZones"][0]["boundaryPoints"]
for boundaryPoint in boundaryPoints:
    FENCE(boundaryPoint['latitude'], boundaryPoint['longitude'], (mission["flyZones"][0]['altitudeMax'])/3.28084, len(boundaryPoints))

file.close() # Close File

# ------------------------------------------------------------------------------------------------------------------

# Mapping Polygon File
file = open("mapping.poly", "w+")

map_height = mission["mapHeight"]/3.28084
map_width = ((16.0/9.0)*map_height)
map_cent_lat, map_cent_long = mission["mapCenterPos"]['latitude'], mission["mapCenterPos"]['longitude']

# Convert Center UTM to Center XY
utm_zone = math.floor((map_cent_long + 180)/6)+1 # Calculate UTM Zone for Conversion
utm_xy_conv = Proj(proj='utm',zone=utm_zone, ellps='WGS84') # Setup Conversion Parameters

map_cent_x, map_cent_y = utm_xy_conv(map_cent_long, map_cent_lat)

# Calculate Four Vertices in XY
map_north_y, map_south_y = map_cent_y + map_height/2, map_cent_y - map_height/2
map_east_x, map_west_x = map_cent_x + map_width/2, map_cent_x - map_width/2

# Convert Four Vertise to UTM
map_east_long, map_north_lat = utm_xy_conv(map_east_x, map_north_y, inverse=True)
map_west_long, map_south_lat = utm_xy_conv(map_west_x, map_south_y, inverse=True)

POLYGON(map_north_lat, map_east_long)
POLYGON(map_north_lat, map_west_long)
POLYGON(map_south_lat, map_west_long)
POLYGON(map_south_lat, map_east_long)
  
file.close() # Close File

# ------------------------------------------------------------------------------------------------------------------

# Search Area File
file = open("searcharea.poly", "w+")
       
boundaries = mission["searchGridPoints"]
for boundary in boundaries:
    POLYGON(boundary['latitude'], boundary['longitude'])
                            
file.close() # Close File
