import pytest
def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true",
                     help="run slow tests")

def pytest_runtest_setup(item):
    if 'slow' in item.keywords and not item.config.getvalue("runslow"):
        pytest.skip("need --runslow option to run")

''' def pytest_namespace():
    return {'path' :'H:/Code/com.itheramedical.PresetEditor/testdata/256Arc-4MHz_Hb, HbO2, Melanin, ICG_v1.2.xml'} '''
