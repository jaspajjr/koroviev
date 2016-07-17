import pytest
import sys, os
sys.path.append(os.path.join(os.path.expanduser('~'), 'working', 'github'))

from koroviev import projections

def test_unpack_cmigc_kwargs_N_default():
    # arrange
    kwargs = {}
    # act
    cmigc_dict = projections.unpack_cmigc_kwargs(kwargs)

    # assert
    assert cmigc_dict['N'] == 10
