import pandas as pd
df_retail= pd.read_csv('retailer extract.csv',sep=';')
df_shop=pd.read_csv('references_initialized_in_shop.csv',sep=';')
#droping empty row in df_retail
df_retail=df_retail.dropna(subset=['EAN'])

# merging on ean
#df represent all the reference yracked by the app and in the store but its weird lemme check that
df=df_shop.merge(df_retail,left_on='reference_id',right_on='EAN')

#some referenced products are not present in the retail csv
# checking for duplicated ids

# Les codes barres sont unique par allee, deux produits dans deux rayons differents peuvent avoir le meme code barre
# un produit peut etre tracké mais en rupture de stock.


# renaming for simplicity
print('Je suis parti du principe qu il était normal que certains produits referencés dans l app ne soit pas present dans les stock et que deux produits puissent avoir le meme EAN mais etre dans deux rayons differents')
print("number of reference not tracked by the app:",len(df_retail.index)-len(df.index))

#getting all the relevant products
#df_retail=df_retail.drop([df_retail['Date déréf']!='Nan'])
df_retail_filtered=df_retail[df_retail['Date déréf.'].isna()]



df_tracked_lib=pd.DataFrame()

df_tracked_lib=df['Libellé  Sous-Famille '].drop_duplicates()
list_of_tracked_lib=df_tracked_lib.values.tolist()


#df_retail_filtered=df_retail_filtered[df_retail_filtered.['Libellé  Sous-Famille '] in list_of_tracked_lib]
for i in df_retail_filtered.index :
    if not df_retail_filtered.loc[i,'Libellé  Sous-Famille '] in list_of_tracked_lib:
        df_retail_filtered=df_retail_filtered.drop(i)



#thats the product that shouldb e tracked
df_merged=df_shop.merge(df_retail_filtered,left_on='reference_id',right_on='EAN',how='right')

df_should_be_tracked=df_merged[df_merged.reference_id.isna()]

df_s_clean=pd.DataFrame()
df_s_clean['Article Libellé Long']=df_should_be_tracked['Article Libellé Long']
df_s_clean['EAN']=df_should_be_tracked['EAN']
print('list of items that should be tracked')
print(df_s_clean)

#replacing all negative values for stock by 0
df_should_be_tracked['Stock en quantité'].fillna(0,inplace=True)
for i in df_should_be_tracked.index:
    if '-' in df_should_be_tracked.loc[i,'Stock en quantité'] or ',' in df_should_be_tracked.loc[i,'Stock en quantité']:
        df_should_be_tracked.loc[i,'Stock en quantité']=0
#df_should_be_tracked['Stock en quantité']=df_should_be_tracked.astype({'Stock en quantité':'int32'}).dtypes


print('total size of the list of relevant but not tracked products:',df_should_be_tracked['Stock en quantité'].astype(int).sum())