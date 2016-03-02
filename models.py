from peewee import *
database = SqliteDatabase('match.db')

class BaseModel(Model):
    class Meta:
        database = database

class Applicant(BaseModel):
    name = CharField(null=False)
    quality = FloatField(null=False)
    apply = FloatField(null=False)
    visit = FloatField(null=False)
    marketing = FloatField(null=False)
    applylimit = IntegerField(null=True)

class Institution(BaseModel):
    name = CharField(null=False)
    quality = FloatField(null=False)
    application = FloatField(null=False)
    interview = FloatField(null=False)
    marketing = FloatField(null=False)
    interviewlimit = IntegerField(null=True)

class Match(BaseModel):
    app = ForeignKeyField(Applicant)
    inst = ForeignKeyField(Institution)
    req_interview = IntegerField(default=-1, null=True)
    inst_interview = IntegerField(null=True)
    app_rank_inst = IntegerField(null=True)
    inst_rank_app = IntegerField(null=True)
    matched = IntegerField(default=-1, null=True)
