import numpy as np
import random
import shapely.geometry
import shapely.ops
from shapely.geometry import LineString
from lloyd import Field

def generate_random_field(board_size, n_points):
    return Field(points=np.random.randint(board_size, size=(n_points, 2)))


def pick_color():
    colors = ["blue","brown","red","yellow","green","orange","beige","turquoise","pink"]
    random.shuffle(colors)
    return colors[0]

def from_voronoi_to_centroids(indexed_pols):
    dict_points = dict()
    for pol1_id, pol_1 in indexed_pols:
        dict_points[pol1_id] = [pol_1.centroid]
        for pol2_id, pol_2 in indexed_pols:
            if pol_1.touches(pol_2) and pol2_id not in dict_points.keys():
                dict_points[pol1_id].append(pol_2.centroid)

    lines = list()
    for id_pol, pol in indexed_pols:
        if not any([i > 950 or i < 0 for tup in pol.centroid.coords for i in tup]):
            for p in dict_points[id_pol]:
                if not any([i > 950 or i < 0 for tup in p.coords for i in tup]):
                    lines.append(LineString([pol.centroid, p]))

    return list(shapely.ops.polygonize(lines))

def generate_polygon_map(field):
    lines = [shapely.geometry.LineString(field.voronoi.vertices[line]) for line in field.voronoi.ridge_vertices if -1 not in line]
    pols = list(shapely.ops.polygonize(lines))
    indexed_pols = [(i,pol) for i,pol in enumerate(pols)]

    return from_voronoi_to_centroids(indexed_pols)