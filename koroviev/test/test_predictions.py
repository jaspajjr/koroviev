import koroviev as kv
import pytest

def test_make_predictions_returns_list():
    # arrange

    # act
    print dir(kv)
    result = kv.make_predictions()
    # assert
    assert isinstance(result, isinstance)
