from route import Route

class Route_Planner(object):
    
    alpha_value = 1.0
        
    def __init__(self, target):
        self.target = target 
        self.smooth_mode = True
        self.route = []
    
    def create_discretized_route_ccw(self, increment = 1.0):
        if self.route is not None:
            pass
        
    def create_discretized_route_cw(self, increment = 1.0):
        if self.route is not None:
            pass
        
    def smoothen_route():
        pass
    
    # target is [x,y] tuple in distance (meters) relative to robot
    @staticmethod
    def get_route(target, smoothen, increment = 0.25):
        
        route = []
        
        current_pos = [0.0, 0.0]
        
        if x * y >= 0:
            # Loop through x_routes first:
            route.append(build_linear_x_path(target, current_pos, increment))
            current_pos = route[len(route) - 1]
            route.append(build_linear_y_path(target, current_pos, increment))
            
        elif x * y < 0:
            route.append(build_linear_y_path(target, current_pos, increment))
            current_pos = route[len(route) - 1]
            route.append(build_linear_x_path(target, current_pos, increment))
        
    def build_linear_x_path(target, current_pos, increment = 0.25):
        route = []
        
        x_target = target[0]
        y_target = target[1]
        
        current_x = current_pos[0]
        current_y = current_pos[1]
        
        while True:
                if abs(x_target - current_x) < increment
                    if x_target < 0:
                        current_x -= abs(x_target - current_x)
                        route.append([current_x, current_y])
                        break
                        
                    elif x_target > 0:
                        current_x += abs(x_target - current_x)
                        route.append([current_x, current_y])
                        break
                
                if x_target < 0:
                    current_x -= increment
                    route.append([current_x, current_y])
                elif x_target > 0:
                    current_x += increment
                    route.append([current_x, current_y])
        
        return route
    
    def build_linear_y_path(target, current_pos, increment = 0.25):
        route = []
        
        x_target = target[0]
        y_target = target[1]
        
        current_x = current_pos[0]
        current_y = current_pos[1]
        
        while True:
                if abs(y_target - current_y) < increment
                    if y_target < 0:
                        current_x -= abs(y_target - current_y)
                        route.append([current_x, current_y])
                        break
                        
                    elif y_target > 0:
                        current_y += abs(y_target - current_y)
                        route.append([current_x, current_y])
                        break
                
                if y_target < 0:
                    current_y -= increment
                    route.append([current_x, current_y])
                elif y_target > 0:
                    current_y += increment
                    route.append([current_x, current_y])
        
        return route
        
    
class Coordinate(object):
    def __init__(self, x = 0.0, y = 0.0, ):
        self.x = x
        self.y = y
        
        
        
            
        