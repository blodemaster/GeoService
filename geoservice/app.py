from flask import jsonify, url_for, request, render_template

from geoservice import create_app
from geoservice import tasks


app = create_app()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/geocode', methods=['GET'])
def geocode():
    address = request.args.get('address')
    task = tasks.geocode.delay(address)
    return jsonify({}), 202, {'Location': url_for('geocode_task_status', task_id=task.id)}


@app.route('/geocode/task/<task_id>/status', methods=['GET', 'DELETE'])
def geocode_task_status(task_id):
    task = tasks.geocode.AsyncResult(task_id)
    if request.method == 'GET':
        response = {'task_id': task_id, 'state': task.state}

        if task.state == 'STARTED':
            # job did not start yet
            response.update({
                'eta': 3,
            })
        elif task.state == 'SUCCESS':
            response.update({'result': task.info})
        else:
            pass
            # something went wrong in the background job
        return jsonify(response)
    elif request.method == 'DELETE':
        task.forget()
        return jsonify({}), 204


@app.route('/reverse-geocode', methods=['GET'])
def reverse_geocode():
    raw_coord = request.args.get('coordinate').split(',')
    coord = list(map(float, raw_coord))
    print(coord)
    task = tasks.reverse_geocode.delay(coord)
    return jsonify({}), 202, {'Location': url_for('reverse_geocode_task_status', task_id=task.id)}


@app.route('/reverse-geocode/task/<task_id>/status', methods=['GET', 'DELETE'])
def reverse_geocode_task_status(task_id):
    task = tasks.reverse_geocode.AsyncResult(task_id)
    if request.method == 'GET':
        response = {'task_id': task_id, 'state': task.state}

        if task.state == 'PENDING':
            # job did not start yet
            response.update({
                'eta': 3,
            })
        elif task.state == 'SUCCESS':
            response.update({'result': task.info})
        else:
            pass
            # something went wrong in the background job
        return jsonify(response)

    elif request.method == 'DELETE':
        task.forget()
        return jsonify({}), 204
