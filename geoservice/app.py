from flask import jsonify, url_for, request, render_template

from geoservice import create_app
from geoservice import tasks


app = create_app()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/geocode', methods=['GET'])
def geocode():
    try:
        address = request.args['address']
        task = tasks.geocode.delay(address)
        return jsonify({}), 202, {'Location': url_for('geocode_task_status', task_id=task.id)}
    except KeyError as e:
        app.logger.error(e)
        return jsonify({'error': 'missing address'}), 400


@app.route('/geocode/task/<task_id>/status', methods=['GET', 'DELETE'])
def geocode_task_status(task_id):
    task = tasks.geocode.AsyncResult(task_id)
    if request.method == 'GET':
        response = {'task_id': task_id, 'state': task.state}

        if task.state == 'SUCCESS':
            if 'error' in task.info:
                response.update(task.info)
            else:
                response.update({'result': task.info})
        else:
            pass
        return jsonify(response)
    elif request.method == 'DELETE':
        task.forget()
        return jsonify({}), 204


@app.route('/reverse-geocode', methods=['GET'])
def reverse_geocode():
    try:
        raw_coord = request.args['coordinate'].split(',')
        coord = list(map(float, raw_coord))
        assert len(coord) == 2 and -90 <= coord[0] <= 90 and -180 <= coord[1] <= 180, f'Invalid input: {coord}'

        task = tasks.reverse_geocode.delay(coord)
        return jsonify({}), 202, {'Location': url_for('reverse_geocode_task_status', task_id=task.id)}
    except KeyError as e:
        app.logger.error(e)
        return jsonify({'error': 'missing coordinate'}), 400
    except AssertionError as e:
        app.logger.error(e)
        return jsonify({'error': 'invalid coordinate'}), 400


@app.route('/reverse-geocode/task/<task_id>/status', methods=['GET', 'DELETE'])
def reverse_geocode_task_status(task_id):
    task = tasks.reverse_geocode.AsyncResult(task_id)
    if request.method == 'GET':
        response = {'task_id': task_id, 'state': task.state}

        if task.state == 'SUCCESS':
            if 'error' in task.info:
                response.update(task.info)
            else:
                response.update({'result': task.info})
        else:
            pass
        return jsonify(response)

    elif request.method == 'DELETE':
        task.forget()
        return jsonify({}), 204
