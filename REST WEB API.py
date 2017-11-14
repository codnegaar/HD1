from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask import Response
from flask import url_for

"""
This program is a REST Web AOI for Basic matrix applications using the Flask  microframework.
1- Design the code using object-oriented principles 
2- Operations: Design the Web API to have the desired operations
3- Exceptions and errors
4- Exceptions and errors: 
5- Properly document the program
6- Appropriate unit test cases should be written for the application using the python unittest module
"""

app = Flask(__name__)

# Define dictionary in order to store json file
matrices = {}

#  Define dictionary to store resultant
dictTMP = {}


class operation_error(Exception):
    pass


@app.route('/')
def welcome_note():
    return "FINAL EXAM REST WEB API"


@app.route('/calculation', methods=['GET', 'POST'])
def calculation():
    """
    :param operation:
    :return:
    """

    if request.method == 'POST':
        matrixTMP = request.json
        # initilize the matrix resultant
        matrices[matrixTMP["resultant"]] = matrixTMP["resultant"]
        # add data to global variable
        dictTMP["datatype"] = matrixTMP["datatype"]
        dictTMP["operationtype"] = matrixTMP["operationtype"]
        # Define other value of dictionary
        dictTMP['op1'] = matrixTMP["operand1"]
        dictTMP['op2'] = matrixTMP["operand2"]
        dictTMP['re'] = matrixTMP["resultant"]
        name1 = dictTMP['op1']
        name2 = dictTMP['op2']

    if not name1 in matrices or name2 not in matrices:
        return jsonify(existence_error)

    if dictTMP["operationtype"] == 'addition':
        # Check the correctness of number of rows and columns of user entries for addition
        if matrices[dictTMP['op1']]['numrows'] == matrices[dictTMP['op2']]['numrows'] and \
                        matrices[dictTMP['op1']]['numcols'] == matrices[dictTMP['op2']]['numcols']:
            output = addition(matrices[dictTMP["op1"]], matrices[dictTMP["op2"]])

            matrices[matrixTMP['resultant']] = \
                {'numrows': len(output), 'numcols': len(output[0], ), 'matrixdata': output}
            # The output stores the outcome of matrix into matrice dictioanry by parameter name
            return jsonify(function_pass)
        else:
            return jsonify(addition_error)

    elif dictTMP["operationtype"] == 'subtraction':
        # Check the correctness of number of rows and columns of user entries for subtraction
        if matrices[dictTMP['op1']]['numrows'] == matrices[dictTMP['op2']]['numrows'] and \
                        matrices[dictTMP['op1']]['numcols'] == matrices[dictTMP['op2']]['numcols']:
            output = subtraction(matrices[dictTMP["op1"]], matrices[dictTMP["op2"]])
            matrices[matrixTMP["resultant"]] = \
                {"numrows": len(output), "numcols": len(output[0], ), "matrixdata": output}

            return jsonify(function_pass)

        else:
            return jsonify(subtraction_error)

    elif dictTMP["operationtype"] == 'multiplication':
        # Check the correctness of number of rows and columns of user entries for multiplication
        if matrices[dictTMP['op1']]['numcols'] == matrices[dictTMP['op2']]['numrows']:
            output = multiply(matrices[dictTMP["op1"]], matrices[dictTMP["op2"]])
            matrices[matrixTMP["resultant"]] = \
                {"numrows": len(output), "numcols": len(output[0], ), "matrixdata": output}
            return jsonify(function_pass)
        else:
            return jsonify(multiplication_error)
    else:
        raise operation_error("Invalid Matrices operation, input(addition, subtraction, or multiplication )")


function_pass = {
    "datatype": "status",
    "statusmessage": "OK",
    "errorcode": 0
}

addition_error = {
    "datatype": "status",
    "statusmessage": "Matrix addition failed due to invalid parameters!)",
    "errorcode": 1
}

subtraction_error = {
    "datatype": "status",
    "statusmessage": "Matrix subtract failed due to invalid parameters!)",
    "errorcode": 2
}

multiplication_error = {
    "datatype": "status",
    "statusmessage": "Matrix multiplication failed due to invalid parameters!",
    "errorcode": 3
}

existence_error = {
    "datatype": "status",
    "statusmessage": "Check the existence of required matrices!",
    "errorcode": 4
}


def addition(matrix1, matrix2):
    x_row = len(matrix1['matrixdata'])
    x_col = len(matrix1['matrixdata'][0])
    y_col = len(matrix2['matrixdata'][0])
    result = [[0 for row in range(y_col)] for col in range(x_row)]
    for i in range(x_col):
        for j in range(y_col):
            result[i][j] = matrix1['matrixdata'][i][j] + matrix2['matrixdata'][i][j]
    return result


def subtraction(matrix1, matrix2):
    x_row = len(matrix1['matrixdata'])
    x_col = len(matrix1['matrixdata'][0])
    y_col = len(matrix2['matrixdata'][0])
    result = [[0 for row in range(y_col)] for col in range(x_row)]
    for i in range(y_col):
        for j in range(x_col):
            result[i][j] = matrix1['matrixdata'][i][j] - matrix2['matrixdata'][i][j]
    return result


def multiply(matrix1, matrix2):
    x_row = len(matrix1['matrixdata'])
    x_col = len(matrix1['matrixdata'][0])
    y_col = len(matrix2['matrixdata'][0])
    result = [[0 for row in range(y_col)] for col in range(x_row)]
    for i in range(x_row):
        for j in range(y_col):
            for k in range(x_col):
                result[i][j] += matrix1['matrixdata'][i][k] * matrix2['matrixdata'][k][j]
    return result


@app.route('/senddata', methods=['PUT', 'POST'])  # Sending the matrix data to URL
def sendResponse():
    if request.method == 'PUT':
        return "Can not find data"

    elif request.method == 'POST':
        mat = request.json
        matrices[mat["name"]] = mat["data"]  # add matrices into the global variable in this program
        return jsonify(function_pass)


@app.route('/getmatrix/<matrixname>')  # Receive data by adding the matrix name
def get_matrix(matrixname):
    return jsonify(matrices[matrixname])  # Retur the matrix's keys


@app.route('/matrices/<matrixname>', methods=['DELETE', 'GET'])
def delete_matrix(matrixname):
    matrix_delete = matrices[matrixname]
    matrices.pop(matrixname, None)
    return jsonify(function_pass)


@app.route('/displaymatrix/<matrixname>')
def displayMatrix(matrixname):
    return render_template("display.html", name=matrixname, matrix=matrices[matrixname]["matrixdata"],
                           length=len(matrices[matrixname]["matrixdata"]))


if __name__ == '__main__':
    # app.debug = True  # Uncomment on debugging flask
    app.run()

"""

# Whenever an operation is executed the API should return the following result as a JSON document:

{
    "datatype": "status",
    "statusmessage":"OK",
    "errorcode":0

}


# First matrix
{
   "datatype": "matrix",
   "name": "A",
   "data": {
      "numrows": 2,
      "numcols": 2,
      "matrixdata": [
         [2, 5],
         [3, 6]
      ]
   }
}


# Second matrix 

{
   "datatype": "matrix",
   "name": "B",
   "data": {
      "numrows": 2,
      "numcols": 2,
      "matrixdata": [
         [4, 8],
         [5, 10] 
      ]
   }
}


# change the operation value according to your needs
{
    "datatype": "operation",
    "operationtype": "addition",
    "operand1": "A",
    "operand2": "B",
    "resultant": "C"
}

{
    "datatype": "operation",
    "operationtype": "subtraction",
    "operand1": "A",
    "operand2": "B",
    "resultant": "D"
}

{
    "datatype": "operation",
    "operationtype": "multiplication",
    "operand1": "A",
    "operand2": "B",
    "resultant": "E"
}


"""
