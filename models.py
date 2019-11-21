from config import db
from sqlalchemy.sql import func, desc

user_likes = db.Table("user_likes",
            db.Column("user_like", db.Integer, db.ForeignKey("users.user_id"), primary_key = True),
            db.Column("idea_liked", db.Integer, db.ForeignKey("ideas.idea_id"), primary_key = True)
            )

friends_table = db.Table("friends",
    db.Column("friender_id", db.Integer, db.ForeignKey("users.user_id"), primary_key=True),
    db.Column("friendee_id", db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
)

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key = True)
    f_name = db.Column(db.String(45))
    l_name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    password = db.Column(db.String(255))
    admin_status = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    liked_idea = db.relationship("Idea", secondary = "user_likes")
    friends=db.relationship("User", 
        secondary=friends_table, 
        primaryjoin=user_id==friends_table.c.friendee_id, 
        secondaryjoin=user_id==friends_table.c.friender_id,
        backref="friending")

    def create_admin(self):
        admin = User(
                f_name= "Admin",
                l_name= "Admin",
                email = "admin",
                admin_status = 1,
                password = self)
        db.session.add(admin)
        db.session.commit()                

class Idea(db.Model):
    __tablename__="ideas"
    idea_id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now())
    author_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable = False)
    author = db.relationship("User", foreign_keys = [author_id], backref = "user_ideas", cascade = "all")
    liked_by = db.relationship("User", secondary = "user_likes")
    
# class Follow(db.Model):
#     __tablename__="follows"
#     id=db.Column(db.Integer, primary_key=True)
#     user_id=db.Column(db.Integer, db.ForeignKey("users.user_id"))
#     user=db.relationship("User",backref="likes", cascade="all")
#     user_id=db.Column(db.Integer, db.ForeignKey("users.user_id"))
#     user=db.relationship("User",backref="likes", cascade="all")
#     created_at=db.Column(db.DateTime, server_default=func.now())