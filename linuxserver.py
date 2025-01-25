from flask import Flask, request, jsonify
from linux import LinuxAutomation

app = Flask(__name__)
linux_automation = LinuxAutomation()

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Linux Server is running"})

@app.route('/capture_screen', methods=['GET'])
def capture_screen():
    base64_str, mime_type = linux_automation.capture_fullscreen_jpg_base64()
    # print(mime_type)
    # print(base64_str)
    return jsonify({"data": base64_str, "mime_type": mime_type})

@app.route('/move_mouse_to', methods=['POST'])
def move_mouse_to():
    data = request.get_json()
    x = data.get('x')
    y = data.get('y')
    if x is None or y is None:
        return jsonify({"error": "Missing parameters x or y"}), 400
    linux_automation.move_mouse_to(x, y)
    return jsonify({"message": "success"})

@app.route('/mouse_click', methods=['GET'])
def mouse_click():
    linux_automation.mouse_click()
    return jsonify({"message": "success"})

@app.route('/mouse_leftClick', methods=['GET'])
def mouse_leftClick():
    linux_automation.mouse_leftClick()
    return jsonify({"message": "success"})

@app.route('/mouse_doubleClick', methods=['GET'])
def mouse_doubleClick():
    linux_automation.mouse_doubleClick()
    return jsonify({"message": "success"})

@app.route('/keyboard_input_key', methods=['POST'])
def keyboard_input_key():
    data = request.get_json()
    key = data.get('key')
    if key is None:
        return jsonify({"error": "Missing parameter key"}), 400
    linux_automation.keyboard_input_key(key)
    return jsonify({"message": "success"})

@app.route('/keyboard_input_hotkey', methods=['POST'])
def keyboard_input_hotkey():
    data = request.get_json()
    keys = data.get('keys')
    if keys is None:
        return jsonify({"error": "Missing parameter keys"}), 400
    linux_automation.keyboard_input_hotkey(keys)
    return jsonify({"message": "success"})

@app.route('/keyboard_input_string', methods=['POST'])
def keyboard_input_string():
    data = request.get_json()
    text = data.get('text')
    if text is None:
        return jsonify({"error": "Missing parameter text"}), 400
    linux_automation.keyboard_input_string(text)
    return jsonify({"message": "success"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
