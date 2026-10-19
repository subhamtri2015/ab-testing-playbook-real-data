import math

import numpy as np

from scripts.stats_utils import holm_adjust, srm_test, two_proportion_z_test


def test_two_proportion_z_test():
    result = two_proportion_z_test(2000, 10000, 1900, 10000)
    assert abs(result['diff'] - (-0.01)) < 1e-6
    assert abs(result['p_value'] - 0.074307) < 1e-3


def test_srm_test():
    chi2, p = srm_test([100, 110], [0.5, 0.5])
    assert chi2 > 0
    assert p >= 0


def test_holm_adjust():
    p = [0.03, 0.01, 0.2]
    adj = holm_adjust(p)
    assert len(adj) == 3
    assert all(0 <= x <= 1 for x in adj)
