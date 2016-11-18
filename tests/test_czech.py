#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from perfection.czech import CzechHashBuilder

def test_guarentees():
    duplicated_input = 'guacala'
    unique_len = len(set(duplicated_input))
    info = CzechHashBuilder(duplicated_input)
    assert 2 * unique_len <= info.n <= 3 * unique_len
    assert info.trials_taken <= info.n ** 0.5
