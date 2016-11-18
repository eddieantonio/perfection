#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest

from perfection.forest import ForestGraph, InvariantError


def test_invariants():
    graph = ForestGraph(edges=[(1, 2), (2, 3)])
    graph += (3, 4)

    with pytest.raises(InvariantError):
        graph += (4, 2)

    with pytest.raises(InvariantError):
        graph += (5, 5)
