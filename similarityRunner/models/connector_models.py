"""
Connector models module contains:
 - the base class for connector settings and derived classes.
 - the base class for connector output and derived classes.
"""

import pandas as pd
from pydantic import BaseModel

Output = pd.DataFrame


class ConnectorSettings(BaseModel):
    """
    ConnectorSettings class is a base class for connector settings.
    """

    # here will be common fields for all connectors


class ConnectorOutput(BaseModel):
    """
    ConnectorOutput class is a base class for connector output.
    """

    # here will be common fields for all connectors
