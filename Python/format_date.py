'''
Created on Aug 19, 2025
@author: Hien Tran
'''
from datetime import datetime
from abt import library
from common.identify.harness_action import HarnessAction
from common.reporter import Reporter
from helper.ta_helper import TAActionArgument
from common.errors import TAError

class FormatDateAction(HarnessAction):
    """
    Action template     "date string"   "format in"     "format out"    "return var"
    Convert date string from one format to another.

    Arguments:
    @param  date string (str): Input date string.
    @param  format in (str): Current format of the date string ("%d-%m-%y").
    @param  format out (str): Desired output format ("%m/%Y").
    @param  return var (str): Variable name to store the converted date string.
    """

    def __init__(self):
        super(FormatDateAction, self).__init__()

    def get_action_name(self):
        """
            Get action name.
            @return: Name of the action.
        """
        return "ta convert date format"

    def execute(self):
        try:
            taa = TAActionArgument("date string", "format in", "format out", "return var")
            date_string = taa.get_string_argument(1, "date string")
            format_in = taa.get_string_argument(2, "format in")
            format_out = taa.get_string_argument(3, "format out")
            return_var = taa.get_string_argument(4, "return var", "_format_date")

            # string -> date
            dt = datetime.strptime(date_string, format_in)

            #format lại date theo format out
            format_date = dt.strftime(format_out)
            library.assign(return_var, format_date)

            return True

        except TAError as err:
            err.report()
        except Exception as ex:
            Reporter.report_exception(ex)
        return False