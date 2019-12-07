from redis import StrictRedis
from data.config import redis_config
from slugify import slugify
import simplejson as json
from app.carrier import Carrier


class Core:
    redis = StrictRedis(
        socket_connect_timeout=3,
        **redis_config
    )

    def getTrains(self, source, destination, departure_date):
        journey = 'journey:{source}_{destination}_{departure_date}_cedecko'.format(
            source=slugify(source, separator="_"),
            destination=slugify(destination, separator="_"),
                                departure_date=departure_date
        )

        redis_data = self.redis.get(journey)
        if redis_data:
            return redis_data
        else:
            carrier_util = Carrier()
            carrier_data = carrier_util.get_journeys(source, destination, departure_date)
            carrier_data = json.dumps(carrier_data)
            self.redis.setex(journey,
                             60*60,
                             carrier_data)
            return carrier_data