import pytest
from scanner_handler import CheckQr

# using pytest-mock to mock methods in the tests

#test case: qr has correct length can be found in the db, so method can_add_device will return expected message
@pytest.mark.parametrize("qr, expected_result", [('123', "hallelujah 123"),
                                ('12356', "hallelujah 12356"),
                                ('1235678',"hallelujah 1235678"),
                                ])
def test_check_scanned_device_valid_qr(mocker, qr, expected_result):

    check_qr = CheckQr()
    # mock db to get true 
    mocker.patch.object(check_qr, "check_in_db", return_value=True)
    # mock can_add_device method to check his call
    can_add_device_mock = mocker.patch.object(check_qr, 'can_add_device')

    check_qr.check_scanned_device(qr)

    can_add_device_mock.assert_called_once_with(expected_result)


#test case: qr has incorrect length, but can be found in the db, so method send_error will return "Error: Wrong qr length" message
@pytest.mark.parametrize("qr, expected_error", [('99999999', "Error: Wrong qr length 8"), 
                                                ('abcd', "Error: Wrong qr length 4"),
                                                ('123456', "Error: Wrong qr length 6")
                                                 ])

def test_check_scanned_device_invalid_qr(mocker, qr, expected_error):

    check_qr = CheckQr()

    mocker.patch.object(check_qr, "check_in_db", return_value=True)

    send_error_mock = mocker.patch.object(check_qr, 'send_error')

    mocker.patch.object(check_qr, "check_len_color", return_value=None)

    check_qr.check_scanned_device(qr)

    send_error_mock.assert_called_once_with(expected_error)
 

#test case: qr has correct length, but can't be found in the db, so method send_error will return "Not in DB" message
@pytest.mark.parametrize("qr, expected_error", [('nonexistent_qr', "Not in DB")])

def test_check_scanned_device_not_in_db(mocker, qr, expected_error):

    check_qr = CheckQr()

    mocker.patch.object(check_qr, "check_in_db", return_value=None)

    send_error_mock = mocker.patch.object(check_qr, 'send_error')

    mocker.patch.object(check_qr, "check_len_color", return_value=True)

    check_qr.check_scanned_device(qr)
 
    send_error_mock.assert_called_once_with(expected_error)

