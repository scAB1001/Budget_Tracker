from app import db


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(500), index=True, unique=True)
    start_date = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    rent = db.Column(db.Float)
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlord.id'))

    def __repr__(self):                                    # 2023-11-16 18:14 | :46.387519
        return f'PropertyID: {self.id}   {self.address}, {str(self.start_date)[:16]}, {self.duration} months, £{self.rent}'


class Landlord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), index=True)
    contact_number = db.Column(db.String(20))
    address = db.Column(db.String(500), index=True, unique=True)
    properties = db.relationship(
        'Property', backref='landlord', lazy='dynamic')

    def __repr__(self):
        return f'LandlordID: {self.id}   {self.name}, {self.contact_number}'
