from datetime import timedelta
import math


def get_hits(data, my_location, radius):

    #filter for only storms that became hurricanes
    df_hu = data[data['status'] == 'HU']

    #full list of storms
    hurricane_dt = data

    #sorted by unique storm identifier
    id = df_hu['identifier'].unique()

    # array that will store list of storms that hit location coordinates
    hurricane_history = []

    # iterate through list of coordinates for each storm, checking to see if the paths cross location coordinates
    for ind in id:
        current = hurricane_dt[hurricane_dt['identifier'] == ind]
        initial_reading = current.head(1)

        # determine if storm started South of location coordinates
        starts_South = initial_reading['latitude'] < my_location[0]
        if (starts_South.item() == True):
            coord_name = 'latitude'
            nearest_coord(coord_name, current, my_location, hurricane_history, radius)
        
        #determine if storm started East of location coordinates
        starts_East = initial_reading['longitude'] < my_location[0]
        if (starts_East.item() == True):
            coord_name = 'longitude'
            nearest_coord(coord_name, current, my_location, hurricane_history, radius)
   

    return [hurricane_history, len(id)]
    

def checkCollision(P,Q, x, y, radius): 
    x1 = P['latitude'].item()
    y1 = P['longitude'].item()
    x2 = Q['latitude'].item()
    y2 = Q['longitude'].item()

    # formula for the perpendicular distance of the location (point) to the line
    dist = abs(((y1-y2)*x)+((x2-x1)*y) + (x1*y2) - (x2*y1)) / math.sqrt(((x2-x1)*(x2-x1)) + ((y2-y1)*(y2-y1)))

    if (radius == dist) or (radius > dist): 
       # touches or intersects radius 
        return True
    else: 
       # outside of radius 
        return False

def nearest_coord(coord_name, current, my_location, hurricane_history, radius):
    # get 2 points closest to the location to form a line, then pass these readings to 'checkCollision' to see if line intersects with the radius around our location

    # get first location after crossing latitude (if it crosses)
    mask = current[coord_name] >= my_location[0]
    point_A = current[mask].head(1) 

    # if it crosses, find previous location reading
    if not point_A.empty:
        point_B = current[
            (current['datetime'] >= (point_A['datetime'].item() - timedelta(hours=6))) & (current['datetime'] < point_A['datetime'].item())
            ]

        # data is not always in 6 hour increments so if more than 1 reading in previous 6 hours, take the latest
        point_B = point_B.tail(1)      

        is_hit = checkCollision(point_A, point_B, my_location[0], my_location[1], radius)
        if is_hit:
            hurricane_history.append(point_A['identifier'].item())
    return ""



        


