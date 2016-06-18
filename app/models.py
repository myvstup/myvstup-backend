from app import db 
import numpy as np 

from app import db

class Session:

    def add_points(data):
        print (data)
        result = db.user_points.insert_one( data )
        return result.inserted_id


#class RelevantSpecialization():

#    def get_point(self):

#        unfetched = db().user_points.find( self.id_query )
#        return [i for i in unfetched]

#    def __init__(self,data):

#        self.id_query = {'_id':data['userId']}

#        print (self.id_query)

#        self.query = {}
#        needed_fields = list(data.keys())
#        needed_fields.remove('userId')
#        for prop in needed_fields:
#            if data[prop]!='all' : self.query.update({ prop : data[prop] })

#        self.query.update( {'zno_coef.needed_zno' : { '$all' : list( get_point()[0]['zno'].key() ) } } )

#        print (self.query)

#    def get_spec(self):
        
#        unfetched = db().info.find( self.query )
#        return [i for i in unfetched]


# decide who will count ranges 
# me or V 

#[ { 'cityName' : '',
#    'universityName' : '',
#    'facultatyName': '',
#    'specialityName': '',
#    'score' : 'failScore','uncertaintyScore','middleScore','succeedScore'}, ... ]



#{ 'cityName'        : str,
#  'uniName'         : str,
#  'facultatyName'   : str,
#  'specialityName'  : str,
#  'speciality_id'    : int,
#  'fieldName'        : str,
#  'zno_coef'      : {'needed_zno': ['zno1','zno2',...]
#                     'zno1': float,
#                     'zno2': float,
#                     'zno3': float}
#  'point_median'     : float,
#  'point_min'        : float,
#  'point_mid_median' : float }