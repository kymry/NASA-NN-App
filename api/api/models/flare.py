from ..__init__ import sqldb


class Flare(sqldb.Model):
    id = sqldb.Column(sqldb.String, primary_key=True)
    begin_time = sqldb.Column(sqldb.DateTime)
    peak_time = sqldb.Column(sqldb.DateTime)
    end_time = sqldb.Column(sqldb.DateTime)
    class_type = sqldb.Column(sqldb.String)
    activity_region = sqldb.Column(sqldb.String)

    def __repr__(self):
        return 'flare: {}'.format(self.id)
