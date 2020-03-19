from requests import post

print(post('http://localhost:5000/api/users',
           json={'id':2,
               'name': 'tester',
                 'surname': 'abc',
                 'age': '20',
                 'position': '9_class',
                 'speciality': 'no',
                 'address': 'street',
                 'email': 'test@test',
                 'hashed_password': '12345',
'modified_date': '01.01.01'
                 }).json())

