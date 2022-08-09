# pylint: disable=no-member
# pylint: disable=assignment-from-no-return

from pandas.plotting._matplotlib.style import get_standard_colors
import matplotlib.pyplot as plt
import pandas as pd
import utils.constants as C
import utils.functions as funcs
import numpy as np


data = pd.read_csv(C.COMBINED_DATA_SET_PATH)

print(data.columns)
