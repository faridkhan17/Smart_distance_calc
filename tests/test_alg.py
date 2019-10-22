import pytest

from mypkg.algorithm import read_file
from mypkg.algorithm import fill_na
from mypkg.algorithm import match_specs
from mypkg.algorithm import assigning_weights
import pandas as pd
import numpy as np

'''
def test_read_file():
    df = read_file('data')
    assert(df.shape == (50, 11))
'''

def test_fill_na():
    mock_df = pd.DataFrame(data={'foo': ['aaaa', 'bbb', np.nan], 'boo': ['aaaa', 'dd', 'e']})
    df = fill_na(mock_df, ['foo', 'boo'])
    assert(df['foo'][2] == 'No Address')


def test_match_specs():
    mock_df = pd.DataFrame(data={'foo': ['aaaa', 'bbb', 'ee e'], 'boo': ['aaaa', 'dd', 'e']})
    df = match_specs(mock_df, ['foo', 'boo'])
    assert(df['matching'][0] == 1)


def test_assigning_weights():
    mock_df = pd.DataFrame(data={'foo': [23, 0, 1], 'boo': [40, 1, 1], 'fooo': [22, 0, 0]})
    df = assigning_weights(mock_df, ['foo', 'boo', 'fooo'])
    assert(df['weights'][1] == 100)
