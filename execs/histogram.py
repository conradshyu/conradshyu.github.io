#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import numpy


def run(input: str) -> str:
    j = json.loads(input)
    variables = j["group"]
    rows = j["data"]
    bins = j["bins"]

    if len(variables) != 1:
        raise ValueError("Select exactly one numerical variable.")
    if not rows:
        raise ValueError("Histogram requires at least one observation.")
    if isinstance(bins, bool) or not isinstance(bins, int) or not 1 <= bins <= 1000:
        raise ValueError("Number of bins must be an integer between 1 and 1000.")

    try:
        values = [row[variables[0]] for row in rows]
        if any(value is None or isinstance(value, bool) for value in values):
            raise ValueError("Missing or boolean values are not numerical measurements.")
        values = numpy.asarray(values, dtype=float)
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("Selected variable must contain only numeric values.") from error

    if values.ndim != 1 or not numpy.isfinite(values).all():
        raise ValueError("Selected variable must contain only finite numeric values.")

    counts, edges = numpy.histogram(values, bins=bins)
    if not numpy.isfinite(edges).all() or not (numpy.diff(edges) > 0).all():
        raise ValueError("Values cannot be represented with the selected number of bins.")

    return json.dumps({
        "variable": variables[0],
        "observations": len(values),
        "counts": counts.tolist(),
        "edges": edges.tolist(),
    }, allow_nan=False)
