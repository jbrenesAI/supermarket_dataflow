import pandas as pd
import os


mercadona_df = pd.read_csv(os.path.join(os.getcwd(), r"../../raw_data/mercadona_data.csv"), sep=';')
mercadona_df = mercadona_df[mercadona_df.columns[1:]]

original_shape = mercadona_df.shape
name_split = mercadona_df['product_name'].str.split(',')

mercadona_df['brand'] = name_split.str[-2]
mercadona_df['quantity'] = name_split.str[-1]
mercadona_df['product_name'] = name_split.str[:-2].str.join(',')

print(mercadona_df.head())
name_processed_shape = mercadona_df.shape


print(original_shape, name_processed_shape)