import pytest
import requests
import os

test_creds = {'email': 'testemail@mail.utoronto.ca', 'password': 'tester'}

class Base:

    def __init__(self):
        self.basedir = os.getcwd()
        self.outdir = self.basedir+'/out'
        self.refdir = self.basedir+'/ref'

    def __enter__(self):
        self.create_dirs()
        return self
        

    def __exit__(self, type, value, tb):
        pass

    def create_dirs(self):
        if not os.path.isdir(self.outdir):
            os.mkdir(self.outdir)

    def write_out(self, testname, result):
        with open(self.outdir+'/'+testname+'.out', 'w') as f:
            f.write(result)
        self.diff_check(testname)
        
    def diff_check(self,testname):
        with open('{}/{}.ref'.format(self.refdir, testname) , 'r') as ref:
            with open(self.outdir+'/'+testname+'.out', 'r') as outfile:
                assert ref.read() == outfile.read()



@pytest.mark.parametrize('testname', ['test_register'])
def test_register(testname):
    test_creds = {'email': 'testemail@mail.utoronto.ca', 'password': 'tester'}
    r = requests.post('http://127.0.0.1:5000/register', data = test_creds)
    with Base() as f:
        f.write_out(testname, r.text)