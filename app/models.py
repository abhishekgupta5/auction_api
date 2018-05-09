# app/models.py

from app import db

class Item(db.Model):
    """
    This class represents the auctioned item model
    """
    __tablename__ = 'items'
    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100))
    start_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    end_time = db.Column(db.DateTime)
    start_amount = db.Column(db.Float, default=50.0)
    #highest_bid = db.Column(db.Float, default=start_amount)
    #winner = db.Column()
    image_url = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Item.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Item: {}>".format(self.name)
