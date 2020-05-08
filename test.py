import requests

# Получение всех работ
print(requests.get('http://127.0.0.1:8080/api/jobs').json())
# Корректное получение одной работы
print(requests.get('http://127.0.0.1:8080/api/jobs/1').json())
# Ошибочный запрос на получение одной работы — неверный id
print(requests.get('http://127.0.0.1:8080/api/jobs/999').json())
# Ошибочный запрос на получение одной работы — строка
print(requests.get('http://127.0.0.1:8080/api/jobs/test').json())
# Верный запрос
print(requests.post('http://127.0.0.1:8080/api/jobs',
                    json={'id': 99,
                          'job': '1',
                          'team_leader': 1,
                          'work_size': 1,
                          'collaborators': '1',
                          'is_finished': False}
                    ).json())
# Не передан параметр is_finished
print(requests.post('http://127.0.0.1:8080/api/jobs',
                    json={'id': 7,
                          'job': '1',
                          'team_leader': 1,
                          'work_size': 1,
                          'collaborators': '1'}
                    ).json())
# Работа с существующим id
print(requests.post('http://127.0.0.1:8080/api/jobs',
                    json={'id': 1,
                          'job': '1',
                          'team_leader': 1,
                          'work_size': 1,
                          'collaborators': '1',
                          'is_finished': False}
                    ).json())
# Передача неверного параметра
print(requests.post('http://127.0.0.1:8080/api/jobs',
                    json={'id': 15,
                          'job': '1',
                          'team_leader': 1,
                          'work_size': 1,
                          'collaborators': '1',
                          'is_finished': 123}
                    ).json())
# Убедимся, что работа добавлена
print(requests.get('http://127.0.0.1:8080/api/jobs').json())
# Удалим работу
print(requests.delete('http://127.0.0.1:8080/api/jobs/99').json())
# Несуществующая работа
print(requests.delete('http://127.0.0.1:8080/api/jobs/999').json())
# Ошибочный запрос на удаление работы — строка
print(requests.delete('http://127.0.0.1:8080/api/jobs/test').json())
# Убедимся, что работа удалена
print(requests.get('http://127.0.0.1:8080/api/jobs').json())
# Заменим параметр is_finished у первой работы
print(requests.put('http://127.0.0.1:8080/api/jobs/1',
                   json={'is_finished': True}).json())
# Попытаемся заменить id на существующий
print(requests.put('http://127.0.0.1:8080/api/jobs/1',
                   json={'id': 2}).json())
# Попытаемся заменить несуществующий параметр
print(requests.put('http://127.0.0.1:8080/api/jobs/1',
                   json={'abc': True}).json())
# Попытаемся заменить на значение другого типа
print(requests.put('http://127.0.0.1:8080/api/jobs/1',
                   json={'is_finished': 123}).json())
# Убедимся, что работа изменена
print(requests.get('http://127.0.0.1:8080/api/jobs').json())
