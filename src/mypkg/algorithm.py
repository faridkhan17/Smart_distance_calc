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


def fill_na(df):
    df['alternativeAddress1_of_student'].fillna('No Address', inplace=True)
    df['alternativeAddress2_of_student'].fillna('No Address', inplace=True)
    df['specialties_of_practice'].fillna(0, inplace=True)
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


def match_specs(df):
    match = []
    for i in range(len(df['favoriteSpecialties_of_student'])):
        words = re.split(', |und ', df['favoriteSpecialties_of_student'][i])

        if df['specialties_of_practice'][i] == 0:
            match.append(matching)
            continue
        else:
            target = re.split(', |und ', df['specialties_of_practice'][i])
        matching = len(list(set(words).intersection(target)))
        match.append(matching)

    df['matching'] = match
    return df


def assigning_weights(df):
    weights = []
    for i in range(len(df)):
        weight = (-df['timeDuration'][i]) + (df['matching'][i] * 100) + (df['hasChildren'][i] * 100)
        weights.append(weight)

    df['weights'] = weights
    df = df.sort_values(by='weights', ascending=False)
    return df


def to_csv(df):
    df.to_csv('algorithm_result.csv')

