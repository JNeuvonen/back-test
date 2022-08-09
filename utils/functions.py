# pylint: disable=no-member
import pandas as pd
import numpy as np
import os
from datetime import datetime
import utils.constants as C


def handle_crypto_price_moves(data):

    cols = []
    for col in C.CRYPTO_SYMBOLS:
        for type_of_sma in C.CRYPTO_SMA_TYPES:
            abs_move = data[col +
                            type_of_sma] - data[col + type_of_sma].shift()
            rel_move = data[col +
                            type_of_sma] / data[col + type_of_sma].shift()

            data[col + '_ABS_MOVE' + type_of_sma] = abs_move
            data[col + '_REL_MOVE' + type_of_sma] = rel_move
            cols.append(col + '_ABS_MOVE' + type_of_sma)

    return cols


def handle_crypto_rsi(data):

    cols = []
    for roll_avg in C.SMA_ROLLING_AVERAGES:
        for col in C.CRYPTO_SYMBOLS:
            for type_of_sma in C.CRYPTO_SMA_TYPES:
                delta = data[col + type_of_sma].diff()
                up = delta.clip(lower=0)
                down = -1*delta.clip(upper=0)
                ema_up = up.ewm(com=roll_avg, adjust=False).mean()
                ema_down = down.ewm(com=roll_avg, adjust=False).mean()
                rs = ema_up/ema_down
                data[col + f'_RSI{roll_avg}' +
                     type_of_sma] = 100 - (100/(1+rs))
                cols.append(col + f'_RSI{roll_avg}' +
                            type_of_sma)
    return cols


def handle_rsi(data, rsi_len, symbols, types):
    cols = []
    for days in rsi_len:
        for symbol in symbols:
            for type_of_rsi in types:
                delta = data[symbol + type_of_rsi].diff()
                up = delta.clip(lower=0)
                down = -1*delta.clip(upper=0)
                ema_up = up.ewm(com=days, adjust=False).mean()
                ema_down = down.ewm(com=days, adjust=False).mean()
                rs = ema_up/ema_down
                data[symbol + f'_RSI{days}' +
                     type_of_rsi] = 100 - (100/(1+rs))
                cols.append(symbol + f'_RSI{days}' +
                            type_of_rsi)
    return cols


def handle_gn_rsi(data, rsi_len, types):
    cols = []
    for days in rsi_len:
        for type_of_rsi in types:
            delta = data[type_of_rsi].diff()
            up = delta.clip(lower=0)
            down = -1*delta.clip(upper=0)
            ema_up = up.ewm(com=days, adjust=False).mean()
            ema_down = down.ewm(com=days, adjust=False).mean()
            rs = ema_up/ema_down
            data[f'RSI{days}_' +
                 type_of_rsi] = 100 - (100/(1+rs))
            cols.append(f'RSI{days}_' +
                        type_of_rsi)
    return cols


def read_crypto_dir(path, ticker):

    shift_col = ['High', 'Low', 'Volume', 'Quote asset volume',
                 'Number of trades', 'Taker buy base asset volume',
                 'Taker buy quote asset volume']

    files = []
    for filename in os.listdir(path):
        df = pd.read_csv(path + '/' +
                         filename, index_col=None, header=None)
        files.append(df)
    ret = pd.concat(files, axis=0, ignore_index=True)
    ret.columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
                   'Close time', 'Quote asset volume',
                   'Number of trades', 'Taker buy base asset volume',
                   'Taker buy quote asset volume', 'Ignore']

    for col in shift_col:
        ret[f'Prev_{col}'] = ret[col].shift()
        ret.drop([col], inplace=True, axis=1)

    ret.drop(['Close', 'Close time'], inplace=True, axis=1)
    ret.drop(['Ignore'], inplace=True, axis=1)
    ret = ret.add_prefix(ticker + ' ')
    ret.rename(columns={ticker + ' ' + 'Open time': 'Open time'}, inplace=True)
    return ret


def read_stock_market_dir(path):

    files = []
    for filename in os.listdir(path):
        df = pd.read_csv(path + '/' +
                         filename, index_col=None)

        df['Prev_Open'] = df['Open'].shift()
        df['Prev_Close'] = df['Adj Close'].shift()
        df['Prev_vol'] = df['Volume'].shift()
        df['Prev_high'] = df['High'].shift()
        df['Prev_low'] = df['Low'].shift()

        df.drop(['Close'], inplace=True, axis=1)
        df.drop(['Volume'], inplace=True, axis=1)
        df.drop(['High'], inplace=True, axis=1)
        df.drop(['Low'], inplace=True, axis=1)

        df = df.add_prefix(filename.replace('.csv', '') + ' ')
        df.rename(columns={filename.replace(
            '.csv', '') + ' ' + 'Date': 'Date'}, inplace=True)
        files.append(df)
    ret = pd.concat(files, axis=1)
    return ret


def read_glassnode_dir(path):
    files = []

    timestamp_col = None

    for filename in os.listdir(path):
        df = pd.read_csv(path + '/' +
                         filename)

        timestamp_col = df['timestamp']
        df.drop(['timestamp'], inplace=True, axis=1)
        df = df.add_prefix(filename.replace('-24h.csv', '') + ' ')
        files.append(df)
    ret = pd.concat(files, axis=1)
    ret['timestamp'] = timestamp_col

    return ret


def assign_stock_market_data(df, index, row):
    cols = list(row.columns)
    for col in cols:
        if col != 'Date':
            df.at[index, col] = row[col]


def assign_glassnode_data(df, index, row):
    cols = list(row.columns)
    for col in cols:
        if col != 'timestamp':
            df.at[index, col] = row[col]


def combine_data(stock_market, crypto, glassnode):

    prev_row = stock_market.iloc[0]

    for index, row in crypto.iterrows():

        dt = datetime.fromtimestamp(row['Open time'] / 1000)
        stock_market_row = stock_market.query(f'Date == "{dt.date()}"')
        glassnode_row = glassnode.query(
            f'timestamp == "{dt.date()}T00:00:00Z"')
        if stock_market_row.empty:
            assign_stock_market_data(crypto, index, prev_row)
        else:
            assign_stock_market_data(crypto, index, stock_market_row)
            prev_row = stock_market_row

        assign_glassnode_data(crypto, index, glassnode_row)


def initiate_nan_values(stock_market_data, crypto_data, glassnode_data):
    stock_m = list(stock_market_data.columns)
    glassnode = list(glassnode_data.columns)

    for col in stock_m:
        crypto_data[col] = np.nan

    for col in glassnode:
        crypto_data[col] = np.nan


def clean_column_names(df):
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace('Close', 'Cls')
    df.columns = df.columns.str.replace('of', '')
    df.columns = df.columns.str.replace('Volume', 'Vol')
    df.columns = df.columns.str.replace('volume', 'Vol')
    df.columns = df.columns.str.replace('-', '_')
    df.columns = df.columns.str.replace('price', 'prce')
    df.columns = df.columns.str.replace('percent', 'perc')
    df.columns = df.columns.str.replace('__', '_')
    df.columns = df.columns.str.replace('circulating', 'circ')
    df.columns = df.columns.str.replace('exchange', 'exch')
    df.columns = df.columns.str.replace('position', 'pos')
    df.columns = df.columns.str.replace('balance', 'bal')

    df.columns = df.columns.str.upper()
    df.columns = df.columns.str.replace('TAKER', 'TKR')
    df.columns = df.columns.str.replace('NUMBER', 'NMBR')
    df.columns = df.columns.str.replace('QUOTE', 'QTE')
    df.columns = df.columns.str.replace('BASE', 'BSE')
    df.columns = df.columns.str.replace('PRIT', 'PROFIT')
    df.columns = df.columns.str.replace('HIGH', 'HI')
    df.columns = df.columns.str.replace('LOW', 'LO')
    df.columns = df.columns.str.replace('SUPPLY', 'SUPPL')


def handle_gn_sma_cals(data, sma_len, types):
    cols = []

    for days in sma_len:
        for sma_type in types:
            mean = data[sma_type].rolling(days).mean()
            data[sma_type + '_DIV_' +
                 f'SMA{days}' + sma_type] = data[sma_type] / mean

            cols.append(sma_type + '_DIV_' +
                        f'SMA{days}' + sma_type)

    return cols


def handle_gn_max_calcs(data, max_len, types):
    cols = []

    for days in max_len:
        for type_of_max in types:
            max = data[type_of_max].rolling(days).max()

            data[type_of_max + '_DIV_' + f'MAX{days}_' +
                 type_of_max] = data[type_of_max] / data[f'MAX{days}_' + type_of_max]

            cols.append(type_of_max + '_DIV_' + f'MAX{days}_' +
                        type_of_max)

    return cols


def handle_sma_calcs(data, sma_len, symbols, types):
    cols = []

    for days in sma_len:
        for symbol in symbols:
            for sma_type in types:

                mean = data[symbol +
                            sma_type].rolling(days).mean()

                data[symbol + f'_SMA{days}' + sma_type] = mean
                data[symbol + sma_type + '_DIV_' + symbol +
                     f'_SMA{days}' + sma_type] = data[symbol + sma_type] / mean
                cols.append(symbol + f'_SMA{days}' + sma_type)

                cols.append(symbol + sma_type + '_DIV_' + symbol +
                            f'_SMA{days}' + sma_type)
    return cols


def handle_crypto_sma_calcs(data):
    cols = []

    for roll_avg in C.SMA_ROLLING_AVERAGES:
        for col in C.CRYPTO_SYMBOLS:
            for type_of_sma in C.CRYPTO_SMA_TYPES:
                data[col + f'_SMA{roll_avg}' + type_of_sma] = data[col +
                                                                   type_of_sma].rolling(roll_avg).mean()
                data[col + type_of_sma + '_DIV_' + col + f'_SMA{roll_avg}' +
                     type_of_sma] = data[col + type_of_sma] / data[col + f'_SMA{roll_avg}' + type_of_sma]

                cols.append(col + f'_SMA{roll_avg}' + type_of_sma)
                cols.append(col + type_of_sma + '_DIV_' + col + f'_SMA{roll_avg}' +
                            type_of_sma)
    return cols


def handle_max_calcs(data, max_len, symbols, types):
    cols = []

    for days in max_len:
        for symbol in symbols:
            for type_of_max in types:
                data[symbol + f'_MAX{days}' + type_of_max] = data[symbol +
                                                                  type_of_max].rolling(days).max()

                data[symbol + type_of_max + '_DIV_' + symbol + f'_MAX{days}' +
                     type_of_max] = data[symbol + type_of_max] / data[symbol + f'_MAX{days}' + type_of_max]

                cols.append(symbol + f'_MAX{days}' + type_of_max)
                cols.append(symbol + type_of_max + '_DIV_' + symbol + f'_MAX{days}' +
                            type_of_max)
    return cols


def handle_crypto_low_calcs(data):
    cols = []
    for days in C.HIGH_OF_N_DAYS:
        for col in C.CRYPTO_SYMBOLS:
            for type_of_high in C.CRYPTO_HIGH_TYPES:
                data[col + f'_MIN{days}' + type_of_high] = data[col +
                                                                type_of_high].rolling(days).min()
                data[col + type_of_high + '_DIV_' + col + f'_MIN{days}' +
                     type_of_high] = data[col + type_of_high] / data[col + f'_MIN{days}' + type_of_high]

                cols.append(col + f'_MIN{days}' + type_of_high)
                cols.append(col + type_of_high + '_DIV_' + col + f'_MIN{days}' +
                            type_of_high)

    return cols


def handle_low_calcs(data, low_len, symbols, types):
    cols = []
    for days in low_len:
        for symbol in symbols:
            for type_of_low in types:
                data[symbol + f'_MIN{days}' + type_of_low] = data[symbol +
                                                                  type_of_low].rolling(days).min()
                data[symbol + type_of_low + '_DIV_' + symbol + f'_MIN{days}' +
                     type_of_low] = data[symbol + type_of_low] / data[symbol + f'_MIN{days}' + type_of_low]

                cols.append(symbol + f'_MIN{days}' + type_of_low)
                cols.append(symbol + type_of_low + '_DIV_' + symbol + f'_MIN{days}' +
                            type_of_low)

    return cols


def handle_gn_low_calcs(data, low_len, types):
    cols = []
    for days in low_len:
        for type_of_low in types:
            data[f'MIN{days}_' +
                 type_of_low] = data[type_of_low].rolling(days).min()

            data[type_of_low + '_DIV_' + f'MIN{days}_' +
                 type_of_low] = data[type_of_low] / data[f'MIN{days}_' + type_of_low]

            cols.append(f'MIN{days}_' +
                        type_of_low)
            cols.append(type_of_low + '_DIV_' + f'MIN{days}_' +
                        type_of_low)

    return cols
