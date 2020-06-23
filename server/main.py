from flask import Flask, request, jsonify
import server_funcs as server

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def NxDown():
    print('[MAIN] HOME')
    return "Wecome to NxDownloader :)"


@app.route('/initFactory', methods = ['POST'])
def initFactory():
    print('[MAIN] initFactory')
    req = request.json
    url = req.get('url')
    return jsonify(server.create_factory(url))

@app.route('/joinFactory', methods = ['POST'])
def joinFactory():
    print('[MAIN] joinFactory')
    req = request.json
    factory_id = req.get('factory_id')
    return jsonify(server.join_factory(factory_id))

@app.route('/getWork', methods = ['POST'])
def getWork():
    print('[MAIN] getWork')
    req = request.json
    factory_id = req.get('factory_id')
    worker_id = req.get('worker_id')
    return jsonify(server.get_work(factory_id, worker_id))

@app.route('/submitWork', methods = ['POST'])
def submitWork():
    print('[MAIN] submitWork')
    req = request.json
    factory_id = req.get('factory_id')
    work_id = req.get('work_id')
    server.submit_work(factory_id, work_id)
    return ""

if __name__ == '__main__':
    app.run(host='127.0.0.1', port = '8001',debug = True)