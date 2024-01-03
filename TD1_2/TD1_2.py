import pandas as pd
import matplotlib.pyplot as plt

# with open('evg_esp_veg.envpdiprboucle.json', 'r') as f:
#     d_json = json.load(f)
# print(d_json)
# print(type(d_json))
# print(d_json.keys())
# print(d_json['values'])
# var = d_json['fields']
# rando = d_json['values']
# print(var)
# print(rando[10])
# print(len(var))
# print(len(rando))
# df =pd.DataFrame.from_dict(rando)
# print(df.shape)
# print(df.head())
# print(df.tail())
# print(df.iloc[:,1:2])
# print(df.loc[4])
# print(df['difficulte'].value_counts())
# print(df['temps_parcours'])
# df['temps_parcours_int'] = df['temps_parcours'].str.replace(' min','')
# pd.to_numeric(df['temps_parcours_int'])
# df['temps_parcours_int'] = df['temps_parcours_int'].astype('int64')
# print(df['temps_parcours_int'])
# print(df['temps_parcours_int'].mean())
# print(df.groupby('difficulte')['temps_parcours_int'].mean())
# difficultes = ['facile', 'moyen' , 'difficile']
# plt.bar(difficultes,df['difficulte'].value_counts().sort_index())
# plt.pie(df['difficulte'].value_counts(), labels=difficultes)
# plt.show()    
# df['longueur'] = df['longueur'].str.replace(',','.')
# df['longueur'] = df['longueur'].str.replace(' km','')
# plt.scatter(x = df['nom'],y = df['longueur'])
# plt.title('longeur de les randonnees')
# plt.xlabel('nom randonee')
# plt.ylabel('longueur randonee')
# plt.show()






with open('carcteristiques-2022.csv', newline='', encoding="utf-8") as f:
    file = pd.read_csv(f, sep=';')
df_cara = pd.DataFrame(file)

with open('vehicules-2022.csv', newline='', encoding="utf-8") as f:
    file = pd.read_csv(f, sep=';')
df_vehicules = pd.DataFrame(file)

accidents_lyon = df_cara[df_cara['com'].str.startswith('690')]
# print(len(accidents_lyon))
accidents_velo = df_vehicules[df_vehicules['catv'] == 1]
# print(len(accidents_velo))
accidents_velo_lyon = accidents_lyon.set_index('Accident_Id').join(accidents_velo.set_index('Num_Acc'),how = 'inner')
print(len(accidents_velo_lyon))

accidents_paris = df_cara[df_cara['com'].str.startswith('920')]
accidents_velo_nanterre = accidents_paris.set_index('Accident_Id').join(accidents_velo.set_index('Num_Acc'),how = 'inner')
# print(len(accidents_velo_nanterre))

accidents_velo_nb = [len(accidents_velo_lyon),len(accidents_velo_nanterre)]
accidents_velo_nom = ['lyon' , 'nanterre']
plt.bar(accidents_velo_nom,accidents_velo_nb)
plt.show()
