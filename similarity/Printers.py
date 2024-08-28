"""
File contains printers implementations
"""
from abc import abstractmethod

import pandas as pd


class Printer:
    """
    Base class for all printers
    """

    @abstractmethod
    def print(self, to_print: pd.DataFrame()):
        """
        Print message
        :param to_print: dataframe results to print
        """
        pass


class ConsolePrinter(Printer):
    """
    Print to console
    """

    def print(self, to_print: pd.DataFrame()):
        """
        Print to console
        :param to_print: dataframe results to print
        """
        for index, row in to_print.iterrows():
            print(row)
