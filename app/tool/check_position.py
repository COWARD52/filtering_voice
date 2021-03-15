from app.db.Volume import Volume
import math


class check:
    longitude = None
    latitude = None

    def __init__(self, longitude, latitude):
        self.longitude = float(longitude)
        self.latitude = float(latitude)
        self.point = self.check()

    def check(self):
        volumes = Volume.query.all()
        point = 0
        for volume in volumes:
            point += self.get_point(volume.longitude, volume.latitude)
        return point

    def get_point(self, longitude, latitude):
        self.longitude *= 1000000
        self.longitude %= 10000
        longitude *= 1000000
        longitude %= 10000
        self.latitude *= 1000000
        self.latitude %= 1000
        latitude *= 1000000
        latitude %= 1000

        distance = math.sqrt((self.longitude - longitude) ** 2 + (self.latitude - latitude) ** 2)
        if distance < 237:
            return 1
        else:
            return 0
