BTC_DATA_PATH = './data/binance/btc-1d-klines'
ETH_DATA_PATH = './data/binance/eth-1d-klines'
COMBINED_DATA_SET_PATH = 'combined-dataset.csv'
STOCK_MARKET_DIR_PATH = './data/stock-market-data'
GLASSNODE_DIR_PATH = './data/glassnode'
BTC_SYMBOL = 'BTC'
ETH_SYMBOL = 'ETH'
SYMBOLS = [BTC_SYMBOL, ETH_SYMBOL]
CRYPTO_SMA_TYPES = ['_OPEN', '_PREV_HI', '_PREV_LO',
                    '_PREV_VOL', '_PREV_TKR_BUY_QTE_ASSET_VOL',
                    '_PREV_NMBR_TRADES', '_PREV_TKR_BUY_BSE_ASSET_VOL']

CRYPTO_HIGH_TYPES = ['_OPEN', '_PREV_HI', '_PREV_LO',
                     '_PREV_VOL', '_PREV_TKR_BUY_QTE_ASSET_VOL',
                     '_PREV_NMBR_TRADES', '_PREV_TKR_BUY_BSE_ASSET_VOL']
SMA_ROLLING_AVERAGES = [100, 14, 7]
HIGH_OF_N_DAYS = [100, 14, 7]
