from mercadona_scrapper import MercadonaScrapper
import pandas as pd
import os

scrapper = MercadonaScrapper()
mercadona_raw_data = scrapper.get_products()

mercadona_df = pd.DataFrame.from_dict(mercadona_raw_data)

mercadona_df.to_csv('C:\\Users\\javier.brenes-ext\\Personal\\projects\\supermarket\\supermarket_data\\mercadona_data.csv')

if __name__ == "__main__":
    print("main")