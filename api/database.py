import peewee as pw
import config
from datetime import datetime

db = pw.PostgresqlDatabase(
    config.POSTGRES_DB,
    user=config.POSTGRES_USER, 
    password=config.POSTGRES_PASSWORD,
    host=config.POSTGRES_HOST, 
    port=config.POSTGRES_PORT)

class BaseModel(pw.Model):
    class Meta:
        database = db

class Classify(BaseModel):
    id = pw.IntegerField()
    image = pw.TextField()
    label = pw.TextField()
    conf_score = pw.FloatField()
    user_agent = pw.TextField()
    ip_address = pw.TextField()
    created_at = pw.DateTimeField(default=datetime.now)

    def serialize(self):
        data = {
            'id': self.id,
            'image': self.image,
            'label': self.label,
            'conf_score': float(self.conf_score),
            'user_agent': self.user_agent,
            'ip_address': self.ip_address,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

        return data
    
db.connect()
db.create_tables([Classify])