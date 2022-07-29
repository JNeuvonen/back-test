# pylint: disable=no-member
# pylint: disable=assignment-from-no-return

from pandas.plotting._matplotlib.style import get_standard_colors
import matplotlib.pyplot as plt
import pandas as pd
import utils.constants as C
import utils.functions as funcs

data = pd.read_csv(C.COMBINED_DATA_SET_PATH)


# crypto SMA
new_sma_cols = funcs.handle_crypto_sma_calcs(data)

# crypto Hi
new_max_cols = funcs.handle_crypto_max_calcs(data)

# crypto Lo
new_min_cols = funcs.handle_crypto_low_calcs(data)


# Visualize
ARG_1 = 'ETH_PREV_TKR_BUY_BSE_ASSET_VOL_DIV_ETH_MAX14_PREV_TKR_BUY_BSE_ASSET_VOL'
ARG_2 = 'BTC_OPEN'
ARG_3 = 'TSLA_OPEN'

VAL_1 = data[ARG_1]
VAL_2 = data[ARG_2]
VAL_3 = data[ARG_3]

colors = get_standard_colors(num_colors=3)

ax1 = VAL_1.plot(color=colors[1])
ax2 = ax1.twinx()


ax2.spines['right'].set_position(('axes', 1.0))
VAL_2.plot(ax=ax2)

ax3 = ax1.twinx()
ax3.spines['right'].set_position(('axes', 1.1))
#VAL_3.plot(ax=ax3, color=colors[2])


plt.show()
