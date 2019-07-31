from scanimporter import import_scan

def test_importer():
    testfile = 'testdata\\Scan_1.msot'
    ret = import_scan(testfile)
    assert ret is not None