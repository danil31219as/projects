from requests import post, get, delete

print(get('http://localhost:5000/api/v2/jobs').json())  # правильный
print(get('http://localhost:5000/api/v2/jobs/1').json())  # правильный
print(get('http://localhost:5000/api/v2/jobs/999').json())  # нет id
print(get('http://localhost:5000/api/v2/jobs/q').json())  # буква
from requests import post

print(post('http://localhost:5000/api/v2/jobs',  # корректный
           json={
               'job': 'tester',
               'team_leader': 1,
               'work_size': 1,
               'is_finished': True,
               'collaborators': '1, 2'}).json())

print(post('http://localhost:5000/api/v2/jobs',  # совпадающий id
           json={'id': 1,
                 'job': 'tester_2',
                 'team_leader': 1,
                 'work_size': 10,
                 'is_finished': True,
                 'collaborators': '1, 2'}).json())

print(post('http://localhost:5000/api/v2/jobs',  # пустой
           json={}).json())

print(post('http://localhost:5000/api/v2/jobs',  # пропущен team_leader
           json={'job': 'tester_2',
                 'work_size': 10,
                 'is_finished': True,
                 'collaborators': '1, 2'}).json())

print(delete('http://localhost:5000/api/v2/jobs/999').json())  # нет id
print(delete('http://localhost:5000/api/v2/jobs/2').json())  # правильный
print(delete('http://localhost:5000/api/v2/jobs/w').json())  # буква
