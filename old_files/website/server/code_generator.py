import random, string
class CodeGenerator():
    """
    CodeGenerator class to generate random alpha-numeric codes
    Attributes:
        Existing: List of already existing emails.
    """
    Existing : list
    code_length : int

    def __init__(self, code_length: int):
        self.code_length = code_length
        self.Existing = []


    def generate(self) -> str:
        """
        generates a random unique alpha-numeric code of code_length.
        :return: returns a string of the unique code.
        """ 
        code = ''.join(random.choice(string.ascii_uppercase + 
                                  string.ascii_lowercase + 
                                  string.digits) for _ in range(self.code_length))
        if code not in self.Existing:
            self.Existing.append(code)
            return code
        else:
            return self.generate()


