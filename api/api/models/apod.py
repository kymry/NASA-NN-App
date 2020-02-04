from ..__init__ import sqldb


class Apod(sqldb.Model):
    """ Astronomy Picture of the Day (APOD) """
    date = sqldb.Column(sqldb.Date, primary_key=True)
    explanation = sqldb.Column(sqldb.String)
    media_type = sqldb.Column(sqldb.String)
    title = sqldb.Column(sqldb.String)
    url = sqldb.Column(sqldb.String)
    path = sqldb.Column(sqldb.String)

    def __repr__(self):
        return 'Astronomy Picture of the Dat: {}'.format(self.title)
