#!/usr/bin/env python3

"""pytest for donor"""

from donor import Donor
from donor import DonorCollection
import pytest

def test_donor_class():
    """test donor"""
    d = Donor("Bill Gates", 1000)
    assert d.name == "Bill Gates"
    assert d.donation == [1000]

def test_donorCollection_class():
    """test donor collection"""
    d_c = DonorCollection()
    d_c.add_new_donor("Bill Gates")
    with pytest.raises(ValueError):
        d_c.add_new_donor("Bill Gates")

    d_c.add_donation("Bill Gates", 1234)
    d = d_c.get_donor("Bill Gates")
    assert d.num_donations == 1
    assert d.total_donations == 1234
    assert d.name == "Bill Gates"
