#Base file for taking interop data output and converting to mission planner files. Four files are outputted: UAV_fence, search_area, UAV_mission, and UGV_mission.
mission = input("Paste mission output:")
template = '{0:d}\t{1:d}\t{2:d}\t{3:d}\t{4:.8f}\t{5:.8f}\t{6:.8f}\t{7:.8f}\t{8:.8f}\t{9:.8f}\t{10:.8f}\t{11:d}\n'


#UAV_fence creation(geofence + obstacles)
n=0
obstacles = mission["stationaryObstacles"]
file = open("UAV_fence.waypoints",'w+') 

file.write("QGC WPL 110\n") #base start

#integrating obstacles to UAV_fence
for obstacle in obstacles:
  latitude = mission["stationaryObstacles"][n]['latitude']
  longitude = mission["stationaryObstacles"][n]['longitude']
  radius = (((mission["stationaryObstacles"][n]['radius'])+15)/3.28084)
  height = ((((mission["stationaryObstacles"][n]['height'])-22+15))/3.28084)
  file.write(template.format(n, 0, 3, 5004, radius, 0, 0, 0, latitude, longitude, height, 1,))  
  n = n+1

#integrating geofence to UAV_fence
file.write(template.format(n, 0, 3, 5001, 12, 0.00000000, 0.00000000, 0.00000000, 38.1462694444444, -76.4281638888889, 0.0, 1))
file.write(template.format(n+1, 0, 3, 5001, 12, 0.00000000, 0.00000000, 0.00000000, 38.151625, -76.4286833333333, 0.0, 1))
file.write(template.format(n+2, 0, 3, 5001, 12, 0.00000000, 0.00000000, 0.00000000, 38.1518888888889, -76.4314666666667, 0.0, 1))
file.write(template.format(n+3, 0, 3, 5001, 12, 0.00000000, 0.00000000, 0.00000000, 38.1505944444444, -76.4353611111111, 0.0, 1))
file.write(template.format(n+4, 0, 3, 5001, 12, 0.00000000, 0.00000000, 0.00000000, 38.1475666666667, -76.4323416666667, 0.0, 1))
file.write(template.format(n+5, 0, 3, 5001, 12, 0.00000000, 0.00000000, 0.00000000, 38.1446666666667, -76.4329472222222, 0.0, 1))
file.write(template.format(n+6, 0, 3, 5001, 12, 0.00000000, 0.00000000, 0.00000000, 38.1432555555556, -76.4347666666667, 0.0, 1))
file.write(template.format(n+7, 0, 3, 5001, 12, 0.00000000, 0.00000000, 0.00000000, 38.1404638888889, -76.4326361111111, 0.0, 1))
file.write(template.format(n+8, 0, 3, 5001, 12, 0.00000000, 0.00000000, 0.00000000, 38.1407194444444, -76.4260138888889, 0.0, 1))
file.write(template.format(n+9, 0, 3, 5001, 12, 0.00000000, 0.00000000, 0.00000000, 38.1437611111111, -76.4212055555556, 0.0, 1))
file.write(template.format(n+10, 0, 3, 5001, 12, 0.00000000, 0.00000000, 0.00000000, 38.1473472222222, -76.4232111111111, 0.0, 1))
file.write(template.format(n+11, 0, 3, 5001, 12, 0.00000000, 0.00000000, 0.00000000, 38.1461305555556, -76.4266527777778, 0.0, 1))

file.close() #close UAV_fence


#creation of search area file
n = 0
map_height = mission["mapHeight"]/3.28084
map_width = ((16.0/9.0)*map_height)
map_cent_lat = mission["mapCenterPos"]['latitude']
map_cent_long = mission["mapCenterPos"]['longitude']

map_north_lat = map_cent_lat + (map_height/(2*111111.0))
map_south_lat = map_cent_lat - (map_height/(2*111111.0))
map_east_long = map_cent_long + ((map_width/2)/math.cos(math.radians(map_cent_lat))/111000.0)
map_west_long = map_cent_long - ((map_width/2)/math.cos(math.radians(map_cent_lat))/111000.0)
file = open("searcharea.poly", "w+")
file.write("#saved by Mission Planner 1.3.70" + '\n')

boundaries = mission["searchGridPoints"]
#for boundary in boundaries:
#  latitude = mission["searchGridPoints"][n]['latitude']
#  longitude = mission["searchGridPoints"][n]['longitude'] 
#  file.write(str(latitude))
#  file.write(' ')
#  file.write(str(longitude))
#  file.write('\n')
#  n = n+1

file.write(str(map_north_lat) + ' ' + str(map_east_long) + '\n')
file.write(str(map_north_lat) + ' ' + str(map_west_long) + '\n')
file.write(str(map_south_lat) + ' ' + str(map_west_long) + '\n')
file.write(str(map_south_lat) + ' ' + str(map_east_long) + '\n')
  
file.close() #close search area file


#UAV_mission creation(waypoints + airdrop)
file = open("UAV_mission.waypoints",'w+') 

#setting home locations and takeoff altitude for UAV
file.write("QGC WPL 110\n")
file.write(template.format(0, 0, 0, 16, 0, 0, 0, 0, 38.145228, -76.426905, 0, 1))
file.write(template.format(1, 0, 3, 22, 0, 0, 0, 0, 0, 0, 30.000000, 1))

#addition target waypoints to UAV_mission
n = 0 #two lines before for home location and takeoff
waypoints = mission["waypoints"]
for waypoint in waypoints:
  latitude = mission["waypoints"][n]['latitude']
  longitude = mission["waypoints"][n]['longitude']
  altitude = ((mission["waypoints"][n]['altitude'])-22)/3.28084
  line = template.format(n+2, 0, 3, 16, 0, 0, 0, 0, latitude, longitude, altitude, 1,)  
  file.write(line)
  n = n+1

#adding airdrop to UAV_mission
airdrop_lat = mission["airDropPos"]['latitude']
airdrop_long = mission["airDropPos"]['longitude']
file.write(template.format(n, 0, 3, 16, 3.00000000, 0.00000000, 0.00000000, 0.00000000, airdrop_lat, airdrop_long, 25.908000, 1)) #fly to airdrop location
file.write(template.format(n+1, 0, 3, 183, 11.00000000, 1900.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.000000, 1)) #servo trigger for release
file.write(template.format(n+2,	0, 3, 183, 10.00000000, 900.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.000000, 1)) #start winch lowering
file.write(template.format(n+3,	0, 3, 16, 20.00000000, 0.00000000, 0.00000000, 0.00000000, airdrop_lat, airdrop_long, 25.908000, 1)) #wait over location for delivery
file.write(template.format(n+4,	0, 3, 183, 10.00000000, 2100.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.000000, 1)) #real back winch
file.write(template.format(n+6,	0, 3, 16, 20.00000000, 0.00000000, 0.00000000, 0.00000000, airdrop_lat, airdrop_long, 25.908000, 1)) #wait over location for real back
file.write(template.format(n+5,	0, 3, 183, 10.00000000, 1500.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.000000, 1)) #stop winch
#file.write(template.format(n+8,	0, 3, 20, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.000000, 1)) #end mission with rtl

file.close() #close UAV_mission


#UGV_mission creation
n = 0
file = open("UGV_mission.waypoints", "w+")
file.write("QGC WPL 110\n")

ugv_lat = mission["ugvDrivePos"]['latitude']
ugv_long = mission["ugvDrivePos"]['longitude']

file.write(template.format(0, 1, 3, 16, 0, 0, 0, 0, airdrop_lat, airdrop_long, 0, 1))
file.write(template.format(1, 0, 3, 16, 0, 0, 0, 0, ugv_lat, ugv_long, 0, 1))

file.close() #close UGV_mission
