# -*- coding: utf-8 -*-
from app import db 
import numpy as np 
import json
from bson.objectid import ObjectId
from operator import itemgetter as itmgtr
from collections import OrderedDict
from functools import wraps

_ALPHABET = ['а','б','в','г','ґ','д','е','є','ж','з','и','і','ї',
             'й','к','л','м','н','о','п','р','с','т','у','ф','х',
             'ц','ч','ш','щ','ь','ю','я']

class Tools:

    def get_student_points(data):
        student_points = {}
        for key in list(data['subjects'].keys()):
            if "score" in list(data['subjects'][key].keys()):
                student_points[key] = data['subjects'][key]['score']

        return {'points' :  student_points}

class RelevantSpecialization():

    def __init__(self,data):

        self.dropdowns = {}
        self.certificateScore = data['certificateScore']
        self.student_points = Tools.get_student_points(data)
        self.uni_rank = json.load(open('app/uni_rank.json','r',encoding = 'utf-8-sig'))
        try:
            self.hasTrainingPoints = data['hasTrainingPoints']
            self.hasOlimpicPoints = data['hasOlimpicPoints']
        except KeyError:
            self.hasTrainingPoints = 0
            self.hasOlimpicPoints = 0

        for prop in list(data.keys()):
            if data[prop]!='Україна' and prop not in ['userId','subjects','certificateScore','hasTrainingPoints','hasOlimpicPoints']: 
                self.dropdowns.update({ prop : str(data[prop])})
                
    def query_data(self):
        q = [ 
                { "$project": { 
                        "possible_combinations":
                            {'$setDifference': [
                                    { "$map": { 
                                        "input": "$possible_combinations",
                                        "as": "k",
                                        "in": { 
                                            "$cond": [ 
                                                { "$setIsSubset": [ "$$k", list( self.student_points['points'].keys())] },
                                                "True",
                                                "False"
                                            ] 
                                        } 
                                    }},
                                    ["False"]]},
                        "cityName"       : 1,
                        "universityName" : 1,
                        "facultatyName"  : 1,
                        "specialityName" : 1,
                        "point_min"      : 1,
                        "point_mid_median":1,
                        "point_median"   : 1,
                        "zno_coefs"      : 1,
                        "link"           : 1,
                        "isFreePlaces"   : 1,
                        "fach_tvorch_coefs":1
                                }},
              {"$match" : 
                     { 'possible_combinations': {'$not': {'$size':0}},
                       'isFreePlaces':True
                      },
               }
            ]

        q[1]['$match'].update(self.dropdowns)

        return [i for i in db.info.aggregate(q)]

    def make_response(self,spec_data,score,student_score):

        try : rank = self.uni_rank[spec_data['universityName']]
        except KeyError : rank = 101
        
        responce_dict = { 'cityName'        : spec_data['cityName'],
                          'universityName'  : spec_data['universityName'],
                          'facultatyName'   : spec_data['facultatyName'],
                          'specialityName'  : spec_data['specialityName'],
                          'url'             : spec_data['link'],
                          'specProbability' : score,
                          'universityRank'  : int(rank)}
                          
        if len(spec_data['fach_tvorch_coefs'])!=0:
            responce_dict.update({'examNumber'      : len(spec_data['fach_tvorch_coefs']),
                                  'examScore'       : np.mean(list(spec_data['fach_tvorch_coefs'].values())) })

        return responce_dict

    def count_proba(self):

        specializations_data = []
        relevant_spec = self.query_data()

        for spec_data in relevant_spec:
            # student score is counting here
            student_score = 0; sum_points = 0
            for zno_name in list(self.student_points['points'].keys()):
                try: 
                    student_score += spec_data['zno_coefs'][zno_name] * self.student_points['points'][zno_name]
                    sum_points += spec_data['zno_coefs'][zno_name]
                except KeyError :pass
            student_score += self.certificateScore*(1 - sum_points)
            student_score += self.hasTrainingPoints * 10 + self.hasOlimpicPoints * 10


            # validating calculation
            if student_score > 220 and student_score < 100:
                return { 'wrong_calculation': student_score,
                         'query'            : self.query }
            # checking what prob he belongs
            spec_score = -1
            for points_range in ['point_min','point_mid_median','point_median']:
                if student_score >= spec_data[points_range] :
                    spec_score += 1

            specializations_data += [ self.make_response(spec_data,spec_score,student_score)]
        specializations_data.sort(key=lambda x: (x['specProbability'],-x['universityRank']),
                                  reverse = True)

        if len(specializations_data)==0:
            error = 'Введених ЗНО недостатньо.'
            return {'specializations': [],
                    'errorMessage' : error }
        return { 'specializations' : specializations_data[:100] }

class AutoCompleteData():

    def __init__(self):
        self.arange = dict(zip(_ALPHABET,range(1,len(_ALPHABET)+1)))

    def alpha_sorting(self,data):
        data = sorted(data, key=lambda i:self.arange.get(i['name'][0].lower()))
        return data

    def get_file(self):
        query = db.auto_complete.find({},{'_id':0})
        return [i for i in query if i['name'] not in ['Донецька область','Луганська область']]
