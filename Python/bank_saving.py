'''
Created on Aug 20, 2025
@author: Hien Tran
'''
import math
from abt import library
from common.identify.harness_action import HarnessAction
from common.reporter import Reporter
from helper.ta_helper import TAActionArgument
from common.errors import TAError

class BankSavingAction(HarnessAction):
    """
    Action template     "initial amount money"      "number of month"       "benefit rate"      "return var"
    Calculate the total benefit of saving money in a bank.

        @param  initial amount money (float): The initial amount of money deposited.
        @param  number of month (int): The number of months the money is saved.
        @param  benefit rate (float): Monthly interest rate in percent (%).
        @param  return var (str): Variable name to store the final result.      Default: _saving_result
    """

    def __init__(self):
        super(BankSavingAction, self).__init__()

    def get_action_name(self):
        """
            Get action name.
            @return: Name of the action.
        """
        return "ta bank saving"
    
    def execute(self):
        try:
            taa = TAActionArgument("initial amount money", "number of month", "benefit rate", "return var")
            n_str = taa.get_string_argument(1,"initial amount money")
            k = taa.get_int_argument(2, "number of month")
            t = float(taa.get_string_argument(3, "benefit rate"))
            return_var = taa.get_string_argument(4,"return var", "_saving_result" )

            n = float(n_str.replace(",", "").replace(".",""))

            total = n
            for _ in range(k):
                total += total * t / 100

            format_total = "{:,}".format(int(total))


            library.assign(return_var, format_total)
            return True

        except TAError as err:
            err.report()
        except Exception as ex:
            Reporter.report_exception(ex)
        return False