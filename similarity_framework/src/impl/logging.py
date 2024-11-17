"""
This file contains constants
"""


class WarningEnable:
    """
    Class for warnings
    """

    __enable = True  # warning will be thrown if it is not True
    __timezone = "always"

    def get_status(self) -> bool:
        """
        :returns __enable
        """
        return self.__enable

    def change_status(self, status: bool):
        """
        Change __enable to status
        :param status: to be changed to
        """
        self.__enable = status

    def disable_timezone_warn(self):
        """Change timezone warning to disable"""
        self.__timezone = "ignore"

    def enable_timezone_warn(self):
        """Change timezone warning to disable"""
        self.__timezone = "always"

    def get_timezone(self) -> str:
        """
        :return: __timezone
        """
        return self.__timezone




warning_enable = WarningEnable()
