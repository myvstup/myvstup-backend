from app import db 
import numpy as np 

from app import db

class Session:

    def add_points(data):

        result = db.user_points.insert_one( { 'points' : data } )

        return result.inserted_id


class RelevantSpecialization():

    def get_point(self):

        unfetched = db().user_points.find( self.id_query )
        return [i for i in unfetched]

    def __init__(self,data):

        self.id_query = {'_id':data['userId']}

        self.query = {}
        needed_fields = list(data.keys())
        needed_fields.remove('userId')
        for prop in needed_fields:
            if data[prop]!='all' : self.query.update({ prop : data[prop] })

        self.query.update( {'zno_coef.needed_zno' : { '$all' : list( get_point()[0]['zno'].key() ) } } )

    def get_spec(self):
        
        unfetched = db().info.find( self.query )
        return [i for i in unfetched]

    def make_response(spec_data,score):
        return { 'cityName' : spec_data['cityName'],
                 'universityName' : spec_data['universityName'],
                 'facultatyName': spec_data['facultatyName'],
                 'specialityName': spec_data['specialityName'],
                 'specProbability' : score }

    def count_proba(self):

        specializations_data = []

        student_points = get_point()
        relevant_spec = get_spec()

        for spec_data in relevant_spec:
            # student score is counting here
            student_score = 0
            for zno_name in list(student_points['points'].keys()):
                student_score += spec_data['zno_coef'][zno_name] * student_points['points'][zno_name]
            # checking what prob he belongs
            spec_score = -1
            for points_range in ['point_min','point_mid_median','point_median']:
                if student_score >= relevant_spec[points_range] :
                    spec_score += 1

            specializations_data += [ make_response(spec_data,spec_score)]
        return { 'userId'          : student_points['_id'],
                 'specializations' : specializations_data }

#{ 'userId' : str, 
#  'specializations': [ {
#      'cityName' : str,
#      'universityName' : str,
#      'facultatyName': str,
#      'specialityName': str,
#      'specProbability' : num (-1, 0, 1, 2)
#      }, {...} ...]
#}

# {'_id'     : 'id',
#  'points'  : {'zno_ukr' : 195,
#               'zno_math': 180,
#               'zno_phys': 192 }
# }
#{ 'cityName'        : str,
#  'uniName'         : str,
#  'facultatyName'   : str,
#  'specialityName'  : str,
#  'speciality_id'    : int,
#  'fieldName'        : str,
#  'zno_coef'      : {'needed_zno': ['zno_ukr','zno_math',zno_phys'],
#                     'zno_ukr' : float,
#                     'zno_math': float,
#                     'zno_phys': float}
#  'point_median'     : float,
#  'point_min'        : float,
#  'point_mid_median' : float }