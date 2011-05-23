"""
This module contains indicators:
     Grather      - (Grather)
     GratherEqual - (Grather or Equal)
     Lesser       - (Lesser)
     LesserEqual  - (Lesser or Equal)
"""

import operator
from .base import *


########################################################################
Grather = Filter.partial("Grather",
    """
    """,
    comparator=operator.gt)


########################################################################
GratherEqual = Filter.partial("GratherEqual",
    """
    """,
    comparator=operator.ge)


########################################################################
Lesser = Filter.partial("Lesser",
    """
    """,
    comparator=operator.lt)


########################################################################
LesserEqual = Filter.partial("LesserEqual",
    """
    """,
    comparator=operator.le)

