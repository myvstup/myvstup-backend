from app import db 
import numpy as np 
from app import db
from bson.objectid import ObjectId

class Session:

    def add_points(data):

        result = db.user_points.insert_one( { 'points' : data } )

        return result.inserted_id


class RelevantSpecialization():


    def __init__(self,data):

        self.id_query = {'_id':ObjectId(data['userId'])}

        self.query = {}
        needed_fields = list(data.keys())
        needed_fields.remove('userId')
        for prop in needed_fields:
            if data[prop]!='all' : self.query.update({ prop : data[prop] })

    def make_response(spec_data,score):
        return { 'cityName' : spec_data['cityName'],
                 'universityName' : spec_data['universityName'],
                 'facultatyName': spec_data['facultatyName'],
                 'specialityName': spec_data['specialityName'],
                 'specProbability' : score }

    def count_proba(self):

        specializations_data = []

        u = db.user_points.find( self.id_query )
        student_points = [i for i in u][0]

        self.query.update( {'zno_coefs.needed_zno' : { '$all' : list( student_points['points'].keys() ) } } )

        relevant_spec = [i for i in  db.info.find( self.query)]

        for spec_data in relevant_spec:
            # student score is counting here
            student_score = 0
            for zno_name in list(student_points['points'].keys()):
                student_score += spec_data['zno_coefs'][zno_name] * student_points['points'][zno_name]
            # checking what prob he belongs
            spec_score = -1
            for points_range in ['point_min','point_mid_median','point_median']:
                if student_score >= spec_data[points_range] :
                    spec_score += 1

            specializations_data += [ RelevantSpecialization.make_response(spec_data,spec_score)]
        return { 'userId'          : str(student_points['_id']),
                 'specializations' : specializations_data }
