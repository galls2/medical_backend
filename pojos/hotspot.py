
class HotSpot:
    def __init__(self, long, lat, radius):
        self.long = long
        self.lat = lat
        self.radius = radius

    def __str__(self):
        return 'Hotspot: center is ({long},{lat}) and radius is {radius}.'\
            .format(long=self.long, lat=self.lat, radius=self.radius)