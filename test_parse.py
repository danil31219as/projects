from requests import post, get, delete

print(post('http://localhost:5000/api/v2/users',
           json={'id': 2,
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

print(get('http://localhost:5000/api/v2/users').json())
print(delete('http://localhost:5000/api/v2/users/2').json())
