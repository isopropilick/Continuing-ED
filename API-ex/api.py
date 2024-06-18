from flask import Flask, request, jsonify

app = Flask(__name__)

def gen_number_list(nmin, nmax, ntype):
    if ntype == 'int':
        return [x for x in range(nmin, nmax + 1)]
    elif ntype == 'float':
        return [x * 1.234 for x in range(nmin, nmax + 1)]
    elif ntype == 'prime':
        plist = []
        for n in range(nmin, nmax + 1):
            if n > 1 and all(n % i != 0 for i in range(2, int(n ** 0.5) + 1)):
                plist.append(n)
        return plist
    else:
        return []

@app.route('/numbers', methods=['GET'])
def get_numbers():
    nmin = int(request.args.get('min', 0))
    nmax = int(request.args.get('max', 100))
    ntype = request.args.get('type', 'int')
    return jsonify(gen_number_list(nmin, nmax, ntype))

@app.route('/calculator', methods=['GET'])
def calculator():
    operation = request.args.get('operation')
    num1 = float(request.args.get('num1', 0))
    num2 = float(request.args.get('num2', 0))

    if operation == 'add':
        result = num1 + num2
    elif operation == 'subtract':
        result = num1 - num2
    elif operation == 'multiply':
        result = num1 * num2
    elif operation == 'divide':
        if num2 != 0:
            result = num1 / num2
        else:
            return jsonify({"error": "Cannot divide by zero"}), 400
    else:
        return jsonify({"error": "Invalid operation"}), 400

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
