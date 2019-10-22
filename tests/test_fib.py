import pytest

from mypkg.fibonacci import fibonacci
from mypkg.algorithm import read_file

def test_fib_10():
	assert(fibonacci(10) == 55)

def test_fib_not_20():
	assert(fibonacci(20) != 20)	
	
def reading_file_to_df():
	assert(df.shape == (50, 11))
