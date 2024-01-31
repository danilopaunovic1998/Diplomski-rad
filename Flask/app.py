from flask import Flask, render_template, request
import threading
import time

app = Flask(__name__)

#Globalne promenljive

is_timer_running = False
start_time = None
time_passed = 0
timer_thread = None

def start_timer():
    global is_timer_running, start_time, timer_thread

    if not is_timer_running:
        start_time = time.time() - time_passed
        is_timer_running = True

        def update_timer():
            global time_passed, is_timer_running

            while is_timer_running:
                current_time = time.time()
                time_passed = current_time - start_time
                time.sleep(1)
                print(time_passed)
        
        timer_thread = threading.Thread(target=update_timer)
        timer_thread.daemon = True
        timer_thread.start()

def stop_timer():
    global is_timer_running
    if is_timer_running:
        is_timer_running = False

def format_time(time):
    minutes = int(time // 60)
    seconds = int(time % 60)

    return f"{minutes:02}:{seconds:02}"

@app.route('/')
def index():
    return render_template('index.html', time_passed=format_time(time_passed), is_timer_running=is_timer_running) 

@app.route('/get_time_passed')
def get_time_passed():
    global time_passed
    return str(format_time(time_passed))

@app.route('/toggle_timer', methods=['POST'])
def toggle_timer():
    if request.method == 'POST' :
        if is_timer_running:
            stop_timer()
        else:
            start_timer()
    
    return '', 204

@app.route('/reset_timer', methods=['POST'])
def reset_timer(): 
    global time_passed
    time_passed = 0
    stop_timer()
    return '', 204 

if __name__ == '__main__':
    app.run(debug=True)




