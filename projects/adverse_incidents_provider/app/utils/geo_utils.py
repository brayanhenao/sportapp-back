from shapely import Point
from shapely.geometry import Polygon
import numpy as np

cali_boundary_coords = [
    [-76.8635495958, 3.1194990575],
    [-76.8642836451, 3.8006769776],
    [-76.0888693083, 3.8015092147],
    [-76.088135259, 3.1203318932],
    [-76.8635495958, 3.1194990575],
]


def generate_random_points(num_points, boundary_coords=None):
    if boundary_coords is None:
        boundary_coords = cali_boundary_coords
    boundary_polygon = Polygon(boundary_coords)
    points = []
    while len(points) < num_points:
        min_x, min_y, max_x, max_y = boundary_polygon.bounds
        random_point = Point(np.random.uniform(min_x, max_x), np.random.uniform(min_y, max_y))
        if random_point.within(boundary_polygon):
            points.append(random_point)

    return points
