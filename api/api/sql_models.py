from .__init__ import sqldb


class Sol(sqldb.Model):
    sol = sqldb.Column(sqldb.Integer, primary_key=True)
    average_temperature = sqldb.Column(sqldb.Float)
    high_temperature = sqldb.Column(sqldb.Float)
    low_temperature = sqldb.Column(sqldb.Float)
    horizontal_wind_speed = sqldb.Column(sqldb.Float)
    pressure = sqldb.Column(sqldb.Float)

    def __repr__(self):
        return 'sol: {}'.format(self.sol)


class Flare(sqldb.Model):
    id = sqldb.Column(sqldb.String, primary_key=True)
    begin_time = sqldb.Column(sqldb.DateTime)
    peak_time = sqldb.Column(sqldb.DateTime)
    end_time = sqldb.Column(sqldb.DateTime)
    class_type = sqldb.Column(sqldb.String)
    activity_region = sqldb.Column(sqldb.String)

    def __repr__(self):
        return 'flare: {}'.format(self.id)




