import random, string


class CodeGenerator:
    """
    CodeGenerator class to generate random alpha-numeric codes
    Attributes:
    """


    def generate(code_length) -> str:
        """
        generates a random unique alpha-numeric code of code_length.
        :return: returns a string of the unique code.
        """ 
        code = ''.join(random.choice(string.ascii_uppercase + 
                                  string.ascii_lowercase + 
                                  string.digits) for _ in range(code_length))
        return code
