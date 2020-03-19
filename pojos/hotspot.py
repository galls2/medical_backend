
class HotSpot:
    def __init__(self, lan, lat, radius):
        self.lan = lan
        self.lat = lat
        self.radius = radius

    def __str__(self):
        return 'Hotspot: center is ({lan},{lat}) and radius is {radius}.'\
            .format(lan=self.lan, lat=self.lat, radius=self.radius)