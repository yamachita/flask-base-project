from __project_name__.extensions import db


class BaseORMModel(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime(timezone=True),
                            server_default=db.func.now())
    update_time = db.Column(db.DateTime(timezone=True),
                            onupdate=db.func.now())

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
