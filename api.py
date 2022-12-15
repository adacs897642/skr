import time

import select
import psycopg2
import psycopg2.extensions

from flask import Flask, jsonify, request, Response, make_response
from datetime import datetime
from flask_socketio import SocketIO, emit

from flask_cors import CORS

from settings import *
from models.shared import db
from models.pvalues import Pvalues
from models.syslog import Syslog
from models.objects import Objects
from models.pvalueslog import PvaluesLog
from models.pcoords import Pcoords

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL,
                                                               db=POSTGRES_DB)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*")

# db.app = app
db.init_app(app)
clients = []


@app.route('/api', methods=['GET'])
def index():
    return []


@app.route('/api/vlog', methods=['GET'])
def vlog():
    alias = request.args.get('alias', '', str)
    # print(alias.encode('utf-8'))
    begin = request.args.get('begin', '', str)
    end = request.args.get('end', '', str)
    n = request.args.get('n', 20, int)
    beginT = None
    endT = None
    try:
        if begin:
            beginT = datetime.strptime(begin, '%Y-%m-%d')
    except:
        beginT = None
    try:
        if end:
            endT = datetime.strptime(end, '%Y-%m-%d')
    except:
        endT = None

    try:
        if beginT and endT:
            answer = PvaluesLog.query.filter(PvaluesLog.alias == alias).filter(PvaluesLog.time <= beginT) \
                .filter(PvaluesLog.time >= endT).order_by(PvaluesLog.time.desc()).all()
        elif beginT:
            answer = PvaluesLog.query.filter(PvaluesLog.alias == alias).filter(PvaluesLog.time <= beginT) \
                .order_by(PvaluesLog.time.desc()).limit(n).all()
        elif endT:
            answer = PvaluesLog.query.filter(PvaluesLog.alias == alias) \
                .filter(PvaluesLog.time >= endT).order_by(PvaluesLog.time.desc()).all()
        else:
            answer = PvaluesLog.query.filter(PvaluesLog.alias == alias).order_by(PvaluesLog.time.desc()).limit(n)
        # print(answer)
        return jsonify({
            'alias': answer[0].alias,
            'data': [result.serialized for result in answer]
        })
    except Exception as e:
        print(e, e.args)
        return []


@app.route('/api/value', methods=['GET'])
def value():
    """Обработка запроса вида /api/value?alias=UTF-1 где alias - алиас нужного параметра"""
    alias = request.args.get('alias', '', str)
    try:
        answer = Pvalues.query.filter(Pvalues.alias == alias)
        return jsonify([result.serialized for result in answer])
    except Exception as e:
        print(e, e.args)
        return []


@app.route('/api/syslog', methods=['GET'])
def syslog():
    """Обработка запроса вида /api/syslog?begin=01-01-2021&end=01-01-2022&n=20 где begin - время начала записей,
    end - время окончания записей, n - количество записей"""
    begin = request.args.get('begin', None)
    end = request.args.get('end', None)
    per_page = request.args.get('per_page', 20, int)
    page = request.args.get('page', 1, int)
    print(begin, end)
    total_count = Syslog.query.count()
    try:
        if (begin is not None) & (end is not None):
            begin = datetime.strptime(begin, '%Y-%m-%d')
            end = datetime.strptime(end, '%Y-%m-%d')
            answer = Syslog.query.order_by(Syslog.time.desc()).filter(Syslog.time >= begin) \
                .filter(Syslog.time <= end).limit(per_page).all()
        elif begin is not None:
            begin = datetime.strptime(begin, '%Y-%m-%d')
            answer = Syslog.query.filter(Syslog.time >= begin).order_by(Syslog.time.desc()).limit(per_page).all()
        elif end is not None:
            end = datetime.strptime(end, '%Y-%m-%d')
            answer = Syslog.query.order_by(Syslog.time.desc()).filter(Syslog.time <= end).limit(per_page).all()
        else:
            answer = Syslog.query.order_by(Syslog.time.desc()).paginate(page=page, per_page=per_page, error_out=False)
            # answer = Syslog.query.paginate()
        # print(answer)
        data = jsonify([result.serialized for result in answer])
        # data = [result.serialized for result in answer]
        resp = make_response(data)
        resp.headers['x-total-count'] = total_count
        # resp.data = jsonify([result.serialized for result in answer])
        return resp
    except Exception as e:
        print(e, e.args)
        return []
    # answer = Syslog.query.order_by(Syslog.time.desc()).limit(10).all()


@app.route('/api/objects', methods=['GET'])
def objects():
    """ Обработка запроса вида /api/objects?id=1 где id - порядковый номер объекта (row в базе) """
    id = request.args.get('id', '*', int)
    try:
        answer = ''
        if id == '*':
            answer = Objects.query.order_by(Objects.id.asc()).all()
        elif isinstance(id, int):
            answer = Objects.query.order_by(Objects.id.asc()).filter(Objects.row == id)
        # print(answer)
        return jsonify([result.serialized for result in answer])
    except Exception as e:
        print(e)
        return []


@app.route('/api/pcoords', methods=['GET'])
def pcoords():
    alias = request.args.get('alias', '', str)
    try:
        answer = Pcoords.query.filter(Pcoords.alias == alias)
        return [result.serialized for result in answer]
    except Exception as e:
        print(e, e.args)
    return []


@app.route('/api/describe', methods=['GET'])
def get_obj():
    n = request.args.get('n', '*', int)

    def serialize(item):
        return {
            'alias': item[0],
            'value': item[1],
            'time': item[2],
            'nico': item[3]

        }

    try:
        answer = db.session.query(Objects.obj, Objects.sim).filter(Objects.row == n).distinct()
        # print(answer[0][0], answer[0][1])
        obj = {
            'obj': answer[0][0],
            'sim': answer[0][1],
            # 'items': []
        }
        answer = db.session.query(Objects.alias, Pvalues.value, Pvalues.time, Pcoords.nico) \
            .filter(Objects.row == n) \
            .join(Pvalues, Objects.alias == Pvalues.alias) \
            .join(Pcoords, Objects.alias == Pcoords.alias).order_by(Pvalues.alias.asc()).all()

        obj['items'] = [serialize(result) for result in answer]
        print(obj)
        return obj
    except Exception as e:
        print(e)
        return []
    pass


@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    print(request.sid)
    print("client has connected")
    clients.append(request.sid)
    emit("connect", {"data": f"id: {request.sid} is connected"})


@socketio.on('data')
def handle_message(data):
    """event listener when client types a message"""
    print("data from the front end: ", str(data))
    emit("data", {'data': data, 'id': request.sid}, broadcast=True)


@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    clients.remove(request.sid)
    emit("disconnect", f"user {request.sid} disconnected", broadcast=True)


@socketio.event
def my_custom_event(arg1, arg2, arg3):
    print('received args: ' + arg1 + arg2 + arg3)


def my_other_thread():
    global clients
    conn = psycopg2.connect(database=POSTGRES_DB, host=POSTGRES_HOST, user=POSTGRES_USER, password=POSTGRES_PW)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    curs = conn.cursor()
    curs.execute("SELECT alias FROM objects;")
    for i in curs.fetchall():
        curs.execute(f"LISTEN \"{i[0]}\";")
    curs.execute("LISTEN syslog;")
    curs.close()

    while True:
        if select.select([conn], [], [], 10) == ([], [], []):
            print("Timeout")
        else:
            conn.poll()
            while conn.notifies:
                data = {}
                notify = conn.notifies.pop(0)
                print("Got NOTIFY:", notify.pid, notify.channel, notify.payload)
                curs = conn.cursor()
                msg = ''
                if notify.channel == 'syslog':
                    msg, data = prepare_message_update_syslog(curs, notify.payload)
                else:
                    msg = 'others_update'

                for client_id in clients:
                    send_message(client_id, msg, data)
                    print(f"send data to {client_id, notify.pid, notify.channel, notify.payload, msg, data}")


def send_message(client_id, msg, data):
    socketio.emit(msg, data, room=client_id)
    print('sending message "{}" to client "{}".'.format(data, client_id))


def prepare_message_update_syslog(curs, id_syslog):
    curs.execute("SELECT id, to_char(time,'YYYY-MM-DD HH24:MI:SS'), author, msg, level FROM syslog WHERE id={}".format(
        id_syslog))
    res = curs.fetchall()[0]
    print('res', res)
    data = {
        'id': res[0],
        'time': res[1],
        'author': res[2],
        'msg': res[3],
        'level': res[4]
    }
    return 'syslog_update', data


if __name__ == '__main__':
    # app.run()
    socketio.start_background_task(my_other_thread)
    socketio.run(app, debug=True, port=5000)
    print('test')
