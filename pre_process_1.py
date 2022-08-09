# pylint: disable=no-member
# pylint: disable=assignment-from-no-return

from pandas.plotting._matplotlib.style import get_standard_colors
import matplotlib.pyplot as plt
import pandas as pd
import utils.constants as C
import utils.functions as funcs
import numpy as np

data = pd.read_csv(C.COMBINED_DATA_SET_PATH)


ORIG_COLS = data.columns
COLS_TO_KEEP = data[['BTC_OPEN', 'BTC_PREV_HI',
                     'BTC_PREV_LO', 'ETH_OPEN', 'ETH_PREV_HI', 'ETH_PREV_LO', 'A_SOPR_BTC',
                     'ASOL_BTC', 'BALD_PRCE_BTC',
                     'FEE_RATIO_MULTIPLE_FRM_BTC', 'MARKET_CAP_TO_THERMOCAP_RATIO_BTC',
                     'MSOL_BTC', 'MVRV_RATIO_BTC', 'MVRV_Z_SCORE_BTC',
                     'MVRV_RATIO_ETH', 'MVRV_Z_SCORE_ETH',
                     'NET_UNREALIZED_PROFIT_LOSS_NUPL_ETH',
                     'NET_UNREALIZED_PROFIT_LOSS_NUPL_BTC', 'PERC_SUPPL_IN_PROFIT_BTC',
                     'PERC_SUPPL_IN_PROFIT_ETH', 'PRCE_DRAWDOWN_FROM_ATH_BTC',
                     'PRCE_DRAWDOWN_FROM_ATH_ETH', 'REALIZED_P_L_RATIO_BTC',
                     'REALIZED_PROFITS_TO_VALUE_RPV_RATIO_BTC', 'RELATIVE_UNREALIZED_LOSS_ETH', 'RELATIVE_UNREALIZED_PROFIT_ETH',
                     'RESERVE_RISK_BTC'
                     ]]


GLASSNODE_COLS = []
cols = np.array(data.columns)

for col in cols:
    col_splitted = col.split('_')
    if col_splitted[0] not in C.STOCK_SYMBOLS and col_splitted[0] not in C.CRYPTO_SYMBOLS and col != 'OPEN_TIME':
        GLASSNODE_COLS.append(col)

# SMA
crypto_sma_cols = funcs.handle_sma_calcs(
    data, C.SMA_ROLLING_AVERAGES, C.CRYPTO_SYMBOLS, C.CRYPTO_SMA_TYPES)

stock_sma_cols = funcs.handle_sma_calcs(
    data, C.SMA_ROLLING_AVERAGES, C.STOCK_SYMBOLS, C.STOCK_TYPES)

gn_sma_cols = funcs.handle_gn_sma_cals(
    data, C.SMA_ROLLING_AVERAGES, GLASSNODE_COLS)


# MAX
crypto_max_cols = funcs.handle_max_calcs(
    data, C.HIGH_OF_N_DAYS, C.CRYPTO_SYMBOLS, C.CRYPTO_HIGH_TYPES)

stock_max_cols = funcs.handle_max_calcs(
    data, C.HIGH_OF_N_DAYS, C.STOCK_SYMBOLS, C.STOCK_TYPES)

gn_max_cols = funcs.handle_gn_max_calcs(data, C.HIGH_OF_N_DAYS, GLASSNODE_COLS)


# crypto Lo
crypto_low_cols = funcs.handle_low_calcs(
    data, C.HIGH_OF_N_DAYS, C.CRYPTO_SYMBOLS, C.CRYPTO_HIGH_TYPES)

stock_low_cols = funcs.handle_low_calcs(
    data, C.HIGH_OF_N_DAYS, C.STOCK_SYMBOLS, C.STOCK_TYPES)

gn_low_cols = funcs.handle_gn_low_calcs(data, C.HIGH_OF_N_DAYS, GLASSNODE_COLS)


# crypto price moves
moves = funcs.handle_crypto_price_moves(data)

# crypto rsi
crypto_rsi_cols = funcs.handle_rsi(
    data, C.HIGH_OF_N_DAYS, C.CRYPTO_SYMBOLS, C.CRYPTO_SMA_TYPES)

stock_rsi_cols = funcs.handle_rsi(
    data, C.HIGH_OF_N_DAYS, C.STOCK_SYMBOLS, C.STOCK_TYPES)

gn_rsi_cols = funcs.handle_gn_rsi(data, C.HIGH_OF_N_DAYS, GLASSNODE_COLS)


# sma from rsi

crypto_sma_from_rsi = funcs.handle_gn_sma_cals(
    data, C.SMA_ROLLING_AVERAGES,  crypto_rsi_cols)

stock_sma_from_rsi = funcs.handle_gn_sma_cals(
    data, C.SMA_ROLLING_AVERAGES,  stock_rsi_cols)

gn_sma_from_rsi = funcs.handle_gn_sma_cals(
    data, C.SMA_ROLLING_AVERAGES,  gn_rsi_cols)

# low from rsi

crypto_low_from_rsi = funcs.handle_gn_low_calcs(
    data, C.SMA_ROLLING_AVERAGES,  crypto_rsi_cols)

stock_sma_from_rsi = funcs.handle_gn_low_calcs(
    data, C.SMA_ROLLING_AVERAGES,  stock_rsi_cols)

gn_sma_from_rsi = funcs.handle_gn_low_calcs(
    data, C.SMA_ROLLING_AVERAGES,  gn_rsi_cols)

# max from rsi

crypto_max_from_rsi = funcs.handle_gn_max_calcs(
    data, C.SMA_ROLLING_AVERAGES,  crypto_rsi_cols)

stock_max_from_rsi = funcs.handle_gn_max_calcs(
    data, C.SMA_ROLLING_AVERAGES,  stock_rsi_cols)

gn_max_from_rsi = funcs.handle_gn_max_calcs(
    data, C.SMA_ROLLING_AVERAGES,  gn_rsi_cols)


funcs.clean_column_names(data)

cols = np.array(ORIG_COLS)

dataColsBefore = np.array(data.columns)
data.drop(axis=1, columns=cols, inplace=True)
dataColsAfter = np.array(data.columns)
data = pd.concat([data, COLS_TO_KEEP], axis=1)


data.to_csv('final-dataset.csv', sep=',', index=False)


# Visualize
#ARG_1 = 'BTC_RSI7_PREV_LO'
#ARG_2 = 'BTC_OPEN'
#ARG_3 = 'TSLA_OPEN'
#
#VAL_1 = data[ARG_1]
#VAL_2 = data[ARG_2]
#VAL_3 = data[ARG_3]
#
#
#colors = get_standard_colors(num_colors=3)
#
#ax1 = VAL_1.plot(color=colors[1])
#ax2 = ax1.twinx()
#
#
#ax2.spines['right'].set_position(('axes', 1.0))
# VAL_2.plot(ax=ax2)
#
#ax3 = ax1.twinx()
#ax3.spines['right'].set_position(('axes', 1.1))
##VAL_3.plot(ax=ax3, color=colors[2])
#
#
# plt.show()
