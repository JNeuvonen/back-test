import utils.constants as C
import utils.functions as funcs
import pandas as pd

btc_data = funcs.read_crypto_dir(C.BTC_DATA_PATH, C.BTC_SYMBOL)
eth_data = funcs.read_crypto_dir(C.ETH_DATA_PATH, C.ETH_SYMBOL)

combined_stock_market_data = funcs.read_stock_market_dir(
    C.STOCK_MARKET_DIR_PATH)

combined_glassnode_data = funcs.read_glassnode_dir(C.GLASSNODE_DIR_PATH)
combined_crypto_data = pd.concat([btc_data, eth_data], axis=1)

combined_crypto_data = combined_crypto_data.loc[:, ~
                                                combined_crypto_data.columns
                                                .duplicated()].copy()
combined_crypto_data.fillna(method='bfill', inplace=True)

combined_stock_market_data = combined_stock_market_data.loc[:, ~
                                                            combined_stock_market_data.columns
                                                            .duplicated()].copy()


funcs.initiate_nan_values(combined_stock_market_data,
                          combined_crypto_data, combined_glassnode_data)

funcs.combine_data(combined_stock_market_data,
                   combined_crypto_data, combined_glassnode_data)


combined_crypto_data.drop(['timestamp', 'Date'], inplace=True, axis=1)

combined_crypto_data.columns = combined_crypto_data.columns.str.replace(
    " value", "")

# pylint: disable=E1101
funcs.clean_column_names(combined_crypto_data)

cols = list(combined_crypto_data)


combined_crypto_data.to_csv('combined-dataset.csv', sep=',', index=False)
