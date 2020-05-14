import overpy


api = overpy.Overpass()
result = api.query("""way["highway"](42.049233,-87.678787,42.062927,-87.668608);out;""")
# s: 42.049233 w: -87.678787 n: 42.062927 e:-87.668608
print(len(result.ways))