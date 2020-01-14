from .__init__ import sqldb


class Sol(sqldb.Model):
    sol = sqldb.Column(sqldb.Integer, primary_key=True)
    average_temperature = sqldb.Column(sqldb.Float)
    high_temperature = sqldb.Column(sqldb.Float)
    low_temperature = sqldb.Column(sqldb.Float)
    horizontal_wind_speed = sqldb.Column(sqldb.Float)
    pressure = sqldb.Column(sqldb.Float)

    def __repr__(self):
        return 'sol {}: ' \
               'average temp {}: ' \
               'high temp {}:' \
               'pressure {}'.format(self.sol, self.average_temperature, self.high_temperature, self.pressure)
