#Base file for taking interop data output and converting to mission planner files. Multiple files for the UGV and UAV are outputted.
import math
mission = input("Paste mission output:")
template = '{0:d}\t{1:d}\t{2:d}\t{3:d}\t{4:.8f}\t{5:.8f}\t{6:.8f}\t{7:.8f}\t{8:.8f}\t{9:.8f}\t{10:.8f}\t{11:d}\n'


#UAV fence file creation(geofence + obstacles)
file = open("UAV_fence.waypoints",'w+') 
file.write("QGC WPL 110\n")

#integrating obstacles to uav fence file
n=0
obstacles = mission["stationaryObstacles"]
for obstacle in obstacles:
  latitude = mission["stationaryObstacles"][n]['latitude']
  longitude = mission["stationaryObstacles"][n]['longitude']
  radius = (mission["stationaryObstacles"][n]['radius'])/3.28084
  height = (mission["stationaryObstacles"][n]['height'])/3.28084
  file.write(template.format(n, 0, 0, 5004, radius, 0, 0, 0, latitude, longitude, height, 1,))  
  n += 1
  
#integrating geofence to uav fence file
m=0
boundaryPoints = mission["flyZones"][0]["boundaryPoints"]
for boundaryPoint in boundaryPoints:
  latitude = mission["flyZones"][0]["boundaryPoints"][m]['latitude']
  longitude = mission["flyZones"][0]["boundaryPoints"][m]['longitude']
  height = (mission["flyZones"][0]['altitudeMax'])/3.28084
  file.write(template.format(n, 0, 0, 5001, len(boundaryPoints), 0, 0, 0, latitude, longitude, height, 1,))  
  n += 1
  m += 1

file.close() #close uav file


#creation of mapping file
file = open("mapping.poly", "w+")
file.write("QGC WPL 110\n")

map_height = mission["mapHeight"]/3.28084
map_width = ((16.0/9.0)*map_height)
map_cent_lat = mission["mapCenterPos"]['latitude']
map_cent_long = mission["mapCenterPos"]['longitude']

map_north_lat = map_cent_lat + (map_height/(2*111111.0))
map_south_lat = map_cent_lat - (map_height/(2*111111.0))
map_east_long = map_cent_long + ((map_width/2)/math.cos(math.radians(map_cent_lat))/111000.0)
map_west_long = map_cent_long - ((map_width/2)/math.cos(math.radians(map_cent_lat))/111000.0)

file.write(str(map_north_lat) + ' ' + str(map_east_long) + '\n')
file.write(str(map_north_lat) + ' ' + str(map_west_long) + '\n')
file.write(str(map_south_lat) + ' ' + str(map_west_long) + '\n')
file.write(str(map_south_lat) + ' ' + str(map_east_long) + '\n')
  
file.close() #close mapping file


#creation of search area file
file = open("searcharea.poly", "w+")
file.write("QGC WPL 110\n")

n = 0          
boundaries = mission["searchGridPoints"]
for boundary in boundaries:
  latitude = mission["searchGridPoints"][n]['latitude']
  longitude = mission["searchGridPoints"][n]['longitude'] 
  file.write(str(latitude) + ' ' + str(longitude) + '\n')
  n += 1

file.close() #close search area file


#uav mission file creation(waypoints + airdrop)
file = open("UAV_mission.waypoints",'w+') 
file.write("QGC WPL 110\n")

#setting home locations and takeoff for UAV
file.write(template.format(0, 0, 0, 16, 0, 0, 0, 0, 38.145228, -76.426905, 0, 1))
file.write(template.format(1, 0, 0, 22, 0, 0, 0, 0, 0, 0, 30.5, 1))

#addition of target waypoints to UAV mission
n = 0
waypoints = mission["waypoints"]
for waypoint in waypoints:
  latitude = mission["waypoints"][n]['latitude']
  longitude = mission["waypoints"][n]['longitude']
  altitude = (mission["waypoints"][n]['altitude'])/3.28084
  line = template.format(n+2, 0, 0, 16, 0, 0, 0, 0, latitude, longitude, altitude, 1,)  
  file.write(line)
  n += 1

#adding in airdrop to UAV mission
airdrop_lat = mission["airDropPos"]['latitude']
airdrop_long = mission["airDropPos"]['longitude']
file.write(template.format(n, 0, 3, 16, 3, 0, 0, 0, airdrop_lat, airdrop_long, 30.5, 1)) #fly to airdrop location
file.write(template.format(n+1, 0, 3, 183, 11, 1900, 0, 0, 0, 0, 0, 1)) #release trigger and winch (same port)
file.write(template.format(n+2,	0, 3, 183, 10, 900, 0, 0, 0, 0, 0, 1)) #start winch lowering
file.write(template.format(n+3,	0, 3, 93, 20, 0, 0, 0, 0, 0, 0, 1)) #wait for delivery
file.write(template.format(n+4,	0, 3, 183, 10, 2100, 0, 0, 0, 0, 0, 1)) #real back winch
file.write(template.format(n+5,	0, 3, 93, 20, 0, 0, 0, airdrop_lat, airdrop_long, 30.5, 1)) #wait for real back
file.write(template.format(n+6,	0, 3, 183, 10, 1500, 0, 0, 0, 0, 0, 1)) #stop winch

file.close() #close UAV mission file


#UGV mission file creation
file = open("UGV_mission.waypoints", "w+")
file.write("#saved by Mission Planner 1.3.70" + '\n')

ugv_lat = mission["ugvDrivePos"]['latitude']
ugv_long = mission["ugvDrivePos"]['longitude']

file.write(template.format(0, 1, 3, 16, 0, 0, 0, 0, airdrop_lat, airdrop_long, 0, 1))
file.write(template.format(1, 0, 3, 16, 0, 0, 0, 0, ugv_lat, ugv_long, 0, 1))

file.close() #close UGV mission file
