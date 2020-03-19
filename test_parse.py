from requests import post
import datetime

print(post('http://localhost:5000/api/v2/users',
           json={'id':2,
               'name': 'tester',
                 'surname': 'abc',
                 'age': '20',
                 'position': '9_class',
                 'speciality': 'no',
                 'address': 'street',
                 'email': 'test@test',
                 'hashed_password': '12345',
'modified_date': datetime.datetime.now()
                 }).json())

