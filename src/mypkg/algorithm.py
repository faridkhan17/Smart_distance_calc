#!/usr/bin/python

"""
algorithm
"""

import pandas as pd
import googlemaps
import re


def read_file(path):
    df_student = pd.read_csv(path + '/' + 'students.csv', sep = '\t')
    df_practices = pd.read_csv(path + '/' + 'practices.csv', sep = '\t')
    
    df_student.rename(columns={'id':'id_of_student', 'address':'address_of_student', 'alternativeAddress1':'alternativeAddress1_of_student', 
    'alternativeAddress2':'alternativeAddress2_of_student', 'favoriteSpecialties':'favoriteSpecialties_of_student'}, inplace=True)
    
    df_practices.rename(columns={'id':'id_of_practice', 'address':'address_of_practice', 'specialties':'specialties_of_practice'}, inplace=True)
    
    df = pd.concat([df_student, df_practices], axis=1, sort=False)
    
    df['Pair'] = df['id_of_student'].str.cat(df['id_of_practice'], sep=' - ')
    return df


list_col = ['alternativeAddress1_of_student', 'alternativeAddress2_of_student']


def fill_na(df, list_col):
    for col in list_col:
        df[col].fillna('No Address', inplace=True)
        # df[col].fillna(0, inplace=True)
    return df


def google_api(origins, destinations, travel):
    gmaps = googlemaps.Client(key='*******************************')
    return gmaps.distance_matrix(origins, destinations, mode=travel)["rows"][0]["elements"][0]["duration"]["text"]


def algorithm_1(df):

    time_duration = []

    for i in range(len(df)):
        score = []

        # Mode
        if df['hasCar'][i]:
            travel = "driving"
        else:
            travel = "bicycling"

        origins = df['address_of_practice'][i]
        destinations = df['address_of_student'][i]

        # scoring
        score.append(google_api(origins, destinations, travel))

        if df['alternativeAddress1_of_student'][i] != 'No Address':
            destinations_alt_1 = df['alternativeAddress1_of_student'][i]
            score.append(google_api(origins, destinations_alt_1, travel))

        if df['alternativeAddress2_of_student'][i] != 'No Address':
            destinations_alt_2 = df['alternativeAddress2_of_student'][i]
            score.append(google_api(origins, destinations_alt_2, travel))

        time_duration.append(min(list(map(int, [i.split(' ')[0] for i in score]))))
        # print(min(list(map(int, [i.split(' ')[0] for i in score]))))

    df['timeDuration'] = time_duration
    return df


list_match = ['favoriteSpecialties_of_student', 'specialties_of_practice']


def match_specs(df, list_match):
    match = []
    df[list_match[1]].fillna(0, inplace=True)
    for i in range(len(df)):
        words = re.split(', |und ', df[list_match[0]][i])

        if df[list_match[1]][i] == 0:
            match.append(matching)
            continue
        else:
            target = re.split(', |und ', df[list_match[1]][i])
        matching = len(list(set(words).intersection(target)))
        match.append(matching)

    df['matching'] = match
    return df


list_weights = ['timeDuration', 'matching', 'hasChildren']


def assigning_weights(df, list_weights):
    weights = []
    for i in range(len(df)):
        weight = (-df[list_weights[0]][i]) + (df[list_weights[1]][i] * 100) + (df[list_weights[2]][i] * 100)
        weights.append(weight)

    df['weights'] = weights
    df = df.sort_values(by='weights', ascending=False)
    return df


def to_csv(df):
    df.to_csv('algorithm_result.csv')

