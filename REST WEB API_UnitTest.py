from flask import request
import unittest
import FinalExam as fe
import json


class TestMatrixTests(unittest.TestCase):

    def create_matrix(self, matrix):
        return self.app.post('/senddata', data=json.dumps(matrix), headers=self.headers)

    def get_matrix(self, matrix):
        return self.app.get('/getmatrix/{}'.format(matrix), headers=self.headers)

    def get_response_data(self, response):

        try:
            return json.loads(response.get_data())
        except Exception as e:
            print("Error happened is: {}".format(e))


    def setUp(self):
        self.app = fe.app.test_client()
        self.headers = {"Content-Type": "application/json"}
        self.matrix_A = dict(datatype="matrix", name="A", data=dict(numrows=2, numcols=2, matrixdata=[[1, 3], [2, 6]]))
        self.matrix_B = dict(datatype="matrix", name="B", data=dict(numrows=2, numcols=2, matrixdata=[[2, 4], [3, 5]]))
        self.matrix_A_response = dict(numrows=2, numcols=2, matrixdata=[[1, 3], [2, 6]])
        self.matrix_C_response = dict(numrows=2, numcols=2, matrixdata=[[3, 7], [5, 11]])
        self.matrix_D_response = dict(numrows=2, numcols=2, matrixdata=[[-1, -1], [-1, 1]])
        self.matrix_E_response = dict(numrows=2, numcols=2, matrixdata=[[11, 19], [22, 38]])

        self.cal_addition_data = dict(datatype="operation", operationtype="addition", operand1="A", operand2="B",
                             resultant="C")

        self.cal_subtraction_data = dict(datatype="operation", operationtype="subtraction", operand1="A", operand2="B",
                             resultant="D")

        self.cal_multiplication_data = dict(datatype="operation", operationtype="multiplication", operand1="A", operand2="B",
                             resultant="E")

    def test_0010_senddata(self):
        response = self.create_matrix(self.matrix_A)
        response_data = self.get_response_data(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get("statusmessage"), 'OK')

    def test_0020_getmatrix(self):
        self.create_matrix(self.matrix_A)
        response = self.app.get('/getmatrix/A', headers=self.headers)
        response_data = self.get_response_data(response)
        self.assertEqual(response_data, self.matrix_A_response)

    # Check the calculation / addition
    def test_0030_calculation_addition(self):
        """
        :return:
        """
        self.create_matrix(self.matrix_A)
        self.create_matrix(self.matrix_B)
        response = self.app.post('/calculation', data=json.dumps(self.cal_addition_data), headers=self.headers)
        response_data = self.get_response_data(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get("statusmessage"), 'OK')
        self.assertEqual(self.get_response_data(self.get_matrix("C")), self.matrix_C_response)

    # Check the calculation / subtraction
    def test_0040_calculation_subtraction(self):
        """
        :return:
        """
        self.create_matrix(self.matrix_A)
        self.create_matrix(self.matrix_B)
        response = self.app.post('/calculation', data=json.dumps(self.cal_subtraction_data), headers=self.headers)
        response_data = self.get_response_data(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get("statusmessage"), 'OK')
        self.assertEqual(self.get_response_data(self.get_matrix("D")), self.matrix_D_response)

    # Check the calculation / multiplication
    def test_0050_calculation_multiplication(self):
        """
        :return:
        """
        self.create_matrix(self.matrix_A)
        self.create_matrix(self.matrix_B)
        response = self.app.post('/calculation', data=json.dumps(self.cal_multiplication_data), headers=self.headers)
        response_data = self.get_response_data(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get("statusmessage"), 'OK')
        self.assertEqual(self.get_response_data(self.get_matrix("E")), self.matrix_E_response)

if __name__ == '__main__':
    unittest.main()



"""
Ran 5 tests in 0.287s

OK

"""
