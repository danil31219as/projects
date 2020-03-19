from requests import post, get, delete

print(post('http://localhost:5000/api/v2/users',  # правильный
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
print(post('http://localhost:5000/api/v2/users',  # уже существует
           json={'id': 1,
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
print(get('http://localhost:5000/api/v2/users').json())  # правильный
print(get('http://localhost:5000/api/v2/users/65').json())  # нет такого id
print(delete('http://localhost:5000/api/v2/users/2').json())  # правильный
print(delete('http://localhost:5000/api/v2/users/40').json())  # нет такого id
