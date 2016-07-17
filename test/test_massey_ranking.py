import pytest
import sys, os
sys.path.append(os.path.join(os.path.expanduser('~'), 'working', 'github'))
from koroviev import massey_ranking

def test_main():
    assert massey_ranking.main() == 1
