#!/usr/bin/python

"""
algorithm
"""

import pandas as pd


def read_file(path):
    df_student = pd.read_csv(path + '/' + 'students.csv', sep = '\t')
    df_practices = pd.read_csv(path + '/' + 'practices.csv', sep = '\t')
    
    df_student.rename(columns={'id':'id_of_student', 'address':'address_of_student', 'alternativeAddress1':'alternativeAddress1_of_student', 
    'alternativeAddress2':'alternativeAddress2_of_student', 'favoriteSpecialties':'favoriteSpecialties_of_student'}, inplace=True)
    
    df_practices.rename(columns={'id':'id_of_practice', 'address':'address_of_practice', 'specialties':'specialties_of_practice'}, inplace=True)
    
    df = pd.concat([df_student, df_practices], axis=1, sort=False)
    
    df['Pair'] = df['id_of_student'].str.cat(df['id_of_practice'], sep=' - ')
    return df

