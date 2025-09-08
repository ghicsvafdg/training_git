'''
Created on Aug 19, 2025
@author: Hien Tran
'''
import datetime
from abt import library
from common.identify.harness_action import HarnessAction
from common.reporter import Reporter
from helper.ta_helper import TAActionArgument
from common.errors import TAError

class GetAgeAction(HarnessAction):
    """
    Action template     "year_of_birth"     "return var"          
    Calculate age from year of birth.

    Arguments:
    @param  year_of_birth (int): year of birth.
    @param  return var (str): Variable name to store the calculated age.

    """

    def __init__(self):
        super(GetAgeAction, self).__init__()

    def get_action_name(self):
        """
            Get action name.
            @return: Name of the action.
        """
        return "ta get age"

    def execute(self):
        try:
            taa = TAActionArgument("year_of_birth", "return var")

            year_of_birth = taa.get_non_negative_numeric_argument(1, "year_of_birth")
            return_var = taa.get_string_argument(2, "return var", "age")

            current_year = datetime.datetime.now().year
            age = current_year - year_of_birth + 1

            
            library.assign(return_var, str(age))
            return True

        except TAError as err:
            err.report()
        except Exception as ex:
            Reporter.report_exception(ex)
        return False
