# (c) Jigarvarma2005
# Always welcome of pull requests

from gevent import monkey
monkey.patch_all()

import os
import time
import aria2p
import platform
import threading
from configs import Config
from database import MongoDB
from gevent.pywsgi import WSGIServer
from flask_socketio import SocketIO, emit
from subprocess import Popen as subprocess_run
from geventwebsocket.handler import WebSocketHandler
from flask import Flask, render_template, request, send_from_directory, make_response


app = Flask(__name__)
socketio = SocketIO(app, async_mode='gevent', logger=True, engineio_logger=True)
db = MongoDB(Config.MONGODB_URI)


def aria_start():
    operating_system = platform.system()
    if operating_system == 'Windows':
        cmd = "aria.bat"
    else:
        cmd = "chmod a+x aria.sh; ./aria.sh"
    subprocess_run(cmd, shell=True)
    time.sleep(5) # wait for 5sec to start aria2c
    aria2 = aria2p.API(
        aria2p.Client(host="http://localhost", port=6800, secret="")
    )
    return aria2

aria2 = aria_start()


# Background thread to monitor and emit download status
def monitor_downloads():
    while True:
        downloads = aria2.get_downloads()
        status_items = []
        for download in downloads:
            download_status = download.status if download.total_length != download.completed_length else "complete"
            if (download_status == "complete" and download.name.strip().upper().startswith("[METADATA]")) or download.name == "undefined":
                continue
            if download_status == 'complete':
                file_dir = os.path.join(Config.DOWNLOADS_FOLDER, download.name)
                if not os.path.exists(file_dir):
                    continue
            progress_data = {
            "status": download_status,
            "progress": download.progress,
            'totalLength': download.total_length_string(),
            'completedLength': download.completed_length_string(),
            'download_id': download.gid,
            'eta': download.eta_string(),
            'name': download.name,
            "active": "true" if download.is_active else "false",
            "paused": "true" if download.is_paused else "false",
            "failed": "true" if download.has_failed else "false"
            }
            if download_status != "complete":
                progress_data['downloadSpeed'] = download.download_speed_string()
            status_items.append(progress_data)
        socketio.emit('status_update', {"status_items": status_items}, namespace='/')
        socketio.sleep(7)  # Refresh status every 7 seconds


# Start the background thread when the server is running
@socketio.on('connect', namespace='/')
def start_monitoring_thread():
    print("connect")

# Route to serve the index.html page
@app.route('/', methods=["GET","POST"])
def index():
    is_logged = request.cookies.get('uid', False)
    
    if request.method == 'POST' and not is_logged:
        username = request.form['username']
        password = request.form['password']
        if db.validate_login(username, password):
            #Avoid sharing
            db.delete_cookies(username)
            uid = db.save_cookies(username)
            resp = make_response(render_template('index.html'))
            resp.set_cookie('uid', uid)
            return resp
        else:
            return render_template('login.html', error="username or password inorrect.")

    if is_logged:
        is_success = db.get_cookies(is_logged)
        if is_success:
            return render_template('index.html')

    resp = make_response(render_template('login.html'))
    resp.delete_cookie('uid')
    return resp

# WebSocket event handlers
@socketio.on('download_magnet', namespace='/')
def download_magnet(data):
    uid = data['uid']
    if uid != "":
        is_success = db.get_cookies(uid)
    if not is_success or uid == "":
        emit('cookie_expired', {"msg": "Cookies expired."})
        return
    download_dir = os.path.join(os.getcwd(), Config.DOWNLOADS_FOLDER)
    options = {
        'dir': download_dir,
    }
    magnet_link = data['magnet_link']
    download = aria2.add_magnet(magnet_link, options=options)
    emit('download_started', {'download_id': download.gid, 'file_name': download.name}, broadcast=True)

@socketio.on('perform_task', namespace='/')
def perform_task(data):
    uid = data['uid']
    if uid != "":
        is_success = db.get_cookies(uid)
    if not is_success or uid == "":
        emit('cookie_expired', {"msg": "Cookies expired."})
        return
    task = data["task"]
    if task in ["pause", "resume", "cancelle"]:
        download = aria2.get_download(data["gid"])
        assert download
        if task == "pause":
            download.pause(True)
        elif task == "resume":
            download.resume()
        elif task == "cancelle":
            download.remove(True, True)

@socketio.on('disconnect', namespace='/')
def test_disconnect():
    print('Client disconnected')


@app.route('/download/<path:filename>')
def download_file(filename):
    is_logged = request.cookies.get('uid', False)
    if is_logged:
        is_success = db.get_cookies(is_logged)
    if not is_logged or not is_success:
        return render_template('forbidden.html')
    # Get the absolute path of the requested file
    file_path = os.path.join(Config.DOWNLOADS_FOLDER, filename)
    # Check if the file path is within the downloads folder
    if os.path.isdir(file_path):
        # Get the list of files in the folder
        files = os.listdir(file_path)
        return render_template('folders.html', folder=filename, files=files)
    elif os.path.exists(file_path):
        # Send the file for download
        return send_from_directory(Config.DOWNLOADS_FOLDER, filename, as_attachment=True)
    else:
        return render_template('forbidden.html')


if __name__ == '__main__':
    # Start the background thread for monitoring downloads
    threading.Thread(target=monitor_downloads, daemon=True).start()
    http_server = WSGIServer((Config.BIND_ADDRESS, Config.PORT), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
