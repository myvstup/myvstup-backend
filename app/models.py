# -*- coding: utf-8 -*-
from app import db 
import numpy as np 
import json
from bson.objectid import ObjectId
from operator import itemgetter as itmgtr
from functools import cmp_to_key

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

        for prop in list(data.keys()):
            if data[prop]!='all' and prop not in ['userId','subjects','certificateScore']: 
                self.dropdowns.update({ prop : str(data[prop])})
                
    def query_data(self):

        q = [ 
                { "$project": { 
                        "possible_combinations": { 
                                "$setDifference": [
                                    { "$map": { 
                                        "input": "$possible_combinations",
                                        "as": "k",
                                        "in": { 
                                            "$cond": [ 
                                                { "$setIsSubset": [ "$$k", list( self.student_points['points'].keys()) ] },
                                                "$$k",
                                                False 
                                            ] 
                                        } 
                                    }},
                                    [False]
                                ]},
                        "cityName"       : 1,
                        "universityName" : 1,
                        "facultatyName"  : 1,
                        "specialityName" : 1,
                        "point_min"      : 1,
                        "point_mid_median":1,
                        "point_median"   : 1,
                        "zno_coefs"      : 1,
                                }
              },
              {"$match" : 
                     {'possible_combinations' : {'$not' : {'$size' : 0 }},
                      'possible_combinations.0' : {'$not' : {'$size' : 0 }},

                      }}
            ]
        q[1]['$match'].update(self.dropdowns)
#        self.query = {'isFreePlaces':True}
        return [i for i in db.info.aggregate(q)]

    def make_response(self,spec_data,score):
        try : rank = self.uni_rank[spec_data['universityName']]
        except KeyError : rank = 101
        return { 'cityName'        : spec_data['cityName'],
                 'universityName'  : spec_data['universityName'],
                 'facultatyName'   : spec_data['facultatyName'],
                 'specialityName'  : spec_data['specialityName'],
                 'specProbability' : score,
                 'universityRank'  : int(rank)}

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
            # validating calculation
            if student_score > 200 and student_score < 100:
                return { 'wrong_calculation': student_score,
                         'query'            : self.query }
            # checking what prob he belongs
            spec_score = -1
            for points_range in ['point_min','point_mid_median','point_median']:
                if student_score >= spec_data[points_range] :
                    spec_score += 1

            specializations_data += [ self.make_response(spec_data,spec_score)]
        specializations_data.sort(key=lambda x: (-x['universityRank'],x['specProbability']),
                                  reverse = True)
        test_list = []
        test_list.append({'cityName': 'Cambridge','facultatyName': ' Harvard Business School','specProbability': -1,'specialityName': 'The Entrepreneurial Management',
                     'universityName': 'HARWARD','universityRank': 1, 'url': 'http://www.hbs.edu/faculty/units/em/Pages/default.aspx'})
        test_list.append({'cityName': 'Стокгольм','facultatyName': 'test_fac','specProbability': 0,'specialityName': 'test_spec',
                     'universityName': 'KTH','universityRank': 2})
        test_list.append({'cityName': 'Дубна','facultatyName': 'ФизТех','specProbability': 1,'specialityName': 'теоретическая физика',
                     'universityName': 'Дубна','universityRank': 3})
        test_list.append({'cityName': 'КПИ','facultatyName': 'test_fac','specProbability': 2,'specialityName': 'test_spec',
                     'universityName': 'test_uni','universityRank': 4})

        return { 'specializations' : test_list + specializations_data[:50] }
