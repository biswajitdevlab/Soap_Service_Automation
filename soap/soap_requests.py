#url= 'https://www.crcind.com/csp/samples/%25SOAP.WebServiceInvoke.cls?CLS=SOAP.Demo&OP=AddInteger'
# test_soap_services.py
import csv
import pytest
from soap_clients import SOAPClient  # Assuming you have a SOAPClient module

def load_test_data():
    test_data = []
    with open("test_data/datas.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cleaned_row = {key.strip(): value for key, value in row.items()}
            test_data.append(cleaned_row)
    return test_data

@pytest.mark.parametrize("data", load_test_data())
def test_soap_service(data):
    soap_client = SOAPClient(endpoint="https://www.crcind.com/csp/samples/%25SOAP.WebServiceInvoke.cls?CLS=SOAP.Demo&OP=AddInteger")
    request_body = construct_request_body(data)
    response = soap_client.send_request(request_body)
    assert response.status_code == 200

        # Add assertions based on the expected results in your CSV file
    assert validate_response(response, data)
def construct_request_body(data):
    # Assuming your SOAP service expects two input parameters named 'param1' and 'param2'
    request_body = f"""
        <AddNumbersRequest>
            <param1>{data['Arg1']}</param1>
            <param2>{data['Arg2']}</param2>
        </AddNumbersRequest>
    """
    return request_body

import xml.etree.ElementTree as ET

def validate_response(response, data):
    if response.status_code != 200:
        print(f"SOAP request failed with status code: {response.status_code}")
        print(f"Actual response content:\n{response.content}")
        assert False  # Fail the test if the status code is not 200

    # Assuming your SOAP service responds with an element named 'AddIntegerResult' containing the sum
    expected_sum = int(data['Arg1']) + int(data['Arg2'])

    # Parse the SOAP response content using ElementTree
    try:
        root = ET.fromstring(response.content)
        actual_sum = int(root.find('.//AddIntegerResult').text)
        assert actual_sum == expected_sum
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        print(f"Actual response content:\n{response.content}")
        assert False  # Fail the test if there's an issue with parsing
