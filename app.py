"""
Flask приложение для работы с API "Academy"
"""
from flask import Flask, jsonify, request
from utils import get_group_by_id, get_groups_list

# создаем экземпляр приложения Flask
app = Flask(__name__)

# конфигурация приложения - выключим ascii для поддрежи кириллицы
app.config['JSON_AS_ASCII'] = False

# делаем первый марштрут - для добычи группы по ID
# http://127.0.0.1:5000/group/1
@app.route('/group/<int:group_id>', methods=['GET'])
def get_group(group_id):
    try:
    # получаем группу по ID
        group = get_group_by_id(group_id)
    except DoesNotExist:
        return jsonify({'error': 'Group not found'}), 404
    
    else:
        group_dict = {
            'id': group.id,
            'group_name': group.group_name,
            "created_at": group.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    # если группа не найдена, возвращаем 404
        return jsonify(group_dict), 200

# /group/list/?sort_direction=asc&name_filter=413
# /group/list/
# http://127.0.0.1:5000/group/list/?sort_direction=desc&name_filter=1
@app.route('/group/list/', methods=['GET'])
def list_groups():
    # получаем параметры запроса
    sort_direction = request.args.get('sort_direction', 'asc')
    name_filter = request.args.get('name_filter', "")
    if sort_direction not in ['asc', 'desc']:
        return jsonify({'error': 'Invalid sort direction'}), 400
    
    groups = get_groups_list(sort_direction, name_filter)

    groups_list = []
    for group in groups:
        group_dict = {
            'id': group.id,
            'group_name': group.group_name,
            "created_at": group.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        groups_list.append(group_dict)
    return jsonify(groups_list), 200

# Добыть студента по ID
@app.route("/student/<int:student_id>", methods=["GET"])
def get_student(student_id):
    try:
        student = get_student_by_id(student_id)  # Предполагается, что функция работает с ID студента

    except DoesNotExist:
        return jsonify({"error": "Студент не найден"}), 404
    
    else:
        student_dict = {
            "id": student.id,
            "first_name": student.first_name,
            "middle_name": student.middle_name,
            "last_name": student.last_name,
            "group_id": student.group_id.id,
            "group_name": student.group_id.group_name,
            "created_at": student.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        return jsonify(student_dict), 200


if __name__ == '__main__':
    app.run(debug=True)