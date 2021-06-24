import os
import re



EMAIL_CODE_REGEX = re.compile(r'<p>Your registration code is <strong>(?P<code>[0-9a-zA-Z]{8})</strong></p>')


def filter_code(data):
    return re.sub(EMAIL_CODE_REGEX, '<CODE>', data)


class BaseTester:
    '''
    Parent class for all diff based testing.
    '''

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


    def run(self, testname, result):
        with open('{}/{}.out'.format(self.outdir, testname), 'w') as f:
            f.write(result)
        self.diff_check(testname)
        

    def diff_check(self, testname):
        with open('{}/{}.ref'.format(self.refdir, testname), 'r') as ref, \
            open('{}/{}.out'.format(self.outdir, testname), 'r') as out:
            ref_text = ref.read()
            out_text = out.read()
            if (ref_text == out_text):
                assert True
                os.remove('{}/{}.out'.format(self.outdir, testname))
            else:
                assert ref_text == out_text
