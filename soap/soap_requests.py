# test_soap_service.py
import pytest
import csv
from soap_clients import SOAPClient
import xml.etree.ElementTree as ET
from urllib.parse import quote
 # Assuming you have a SOAPClient module

def load_test_data():
    test_data = []
    with open("test_data/datas.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cleaned_row = {key.strip(): value.strip() for key, value in row.items()}
            test_data.append(cleaned_row)
    return test_data


@pytest.mark.parametrize("data", load_test_data())
def test_soap_service(data):
    soap_client = SOAPClient()

    # Construct the URL and parameters for the GET request
    base_url = "https://www.crcind.com/csp/samples/SOAP.Demo.cls"
    soap_method = "AddInteger"

    # Encode the URL with proper percent encoding
    encoded_url = f"{base_url}?soap_method={quote(soap_method)}&Arg1={quote(data['Arg1'])}&Arg2={quote(data['Arg2'])}"

    # Send a GET request to invoke the SOAP operation
    response = soap_client.send_request(url=encoded_url, method='GET')
    assert response.status_code == 200

    # Validate the response
    assert validate_response(response, data)

def validate_response(response, data):
    try:
        root = ET.fromstring(response.content)
        result_element = root.find('.//{http://tempuri.org}AddIntegerResult')
        actual_sum = int(result_element.text)
        expected_sum = int(data['Arg1']) + int(data['Arg2'])
        print(f"Expected Sum: {expected_sum}, Actual Sum: {actual_sum}")
        if actual_sum != expected_sum:
            print(f"Assertion failed: Expected Sum: {expected_sum}, Actual Sum: {actual_sum}")
            return False
        else:
            print("Assertion passed!")
            return True
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        print(f"Actual response content:\n{response.content}")
        return False
