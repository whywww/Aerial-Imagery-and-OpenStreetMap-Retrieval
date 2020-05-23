import overpy
import cv2
import matplotlib.pyplot as plt

bounding_box = [42.047000, -87.682300, 42.062000, -87.668500]
api = overpy.Overpass()
result = api.query("""
    way(42.047000, -87.682300, 42.062000, -87.668500) ["highway"~"primary|secondary|tertiary|residential|cycleway|path"] ;
    (._;>;);
    out body;
    """)

my_map = cv2.imread('images/my_map.png')
height, width = my_map.shape[0], my_map.shape[1]
lat_step = (bounding_box[2] - bounding_box[0]) / height
long_step = (bounding_box[3] - bounding_box[1]) / width

plt.figure()
plt.imshow(my_map)

for way in result.ways:
    # print("Name: %s" % way.tags.get("name", "n/a"))
    print("  Highway: %s" % way.tags.get("highway", "n/a"))
    lats = []
    lons = []
    for node in way.nodes:
        # print("    Lat: %f, Lon: %f" % (node.lat, node.lon))
        lat = (bounding_box[2] - float(node.lat))/lat_step
        lon = (float(node.lon) - bounding_box[1])/long_step
        if lat < 0 or lon < 0 or lat > height or lon > width:
            continue
        lats.append(lat)
        lons.append(lon)
    plt.plot(lons, lats) # , s=2, c='red', marker='o'
plt.axis('equal')
plt.savefig('images/matched.png')
plt.show()
