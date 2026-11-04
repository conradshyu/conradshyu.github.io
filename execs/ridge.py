#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import numpy
from sklearn import linear_model

def run(input: str) -> str:
    """Fit a Ridge regression model and format its tables and plot data."""
    s = json.loads(input)
    data = s["data"]
    x = [[float(row[k]) for k in s["x"]] for row in data]
    y = [float(row[s["y"][0]]) for row in data]
    alpha = float(s.get("alpha", 1.0))

    if not numpy.isfinite(alpha) or alpha < 0:
        raise ValueError("Alpha must be a finite, non-negative number.")

    model = linear_model.Ridge(alpha=alpha).fit(x, y)
    fitted = model.predict(x)
    predictors = {k: numpy.array([float(row[k]) for row in data]) for k in s["x"]}
    intercept = float(model.intercept_)
    plot_min = min(float(min(fitted)), min(y))
    plot_max = max(float(max(fitted)), max(y))

    return json.dumps({
        "table": {
            "analysis": {
                "thead": "<tr><th style='width: 70%;'>Variable</th><th>Value</th></tr>",
                "tbody": f"<tr><td>Intercept</td><td>{intercept:0.3f}</td></tr>" +
                    f"<tr><td>Alpha</td><td>{alpha:0.3f}</td></tr>" +
                    "".join([f"<tr><td>{name}</td><td>{coef:0.3f}</td></tr>"
                             for name, coef in zip(s["x"], model.coef_)]) +
                    f"<tr><td>R<sup>2</sup> Score</td><td>{model.score(x, y):0.3f}</td></tr>",
            },
            "summary": {
                "thead": "<tr><th style='width: 40%;'>Variable</th><th style='width: 15%;'>Mean</th><th style='width: 15%;'>Variance</th><th style='width: 15%;'>Maximum</th><th>Minimum</th></tr>",
                "tbody": "".join([
                    f"<tr><td>{name}</td><td>{values.mean():0.3f}</td><td>{values.var():0.3f}</td><td>{values.max():0.3f}</td><td>{values.min():0.3f}</td></tr>"
                    for name, values in predictors.items()
                ]),
            },
        },
        "data": {
            "observe": [{"x": float(prediction), "y": actual} for prediction, actual in zip(fitted, y)],
            "predict": [{"x": float(value), "y": float(value)} for value in numpy.linspace(plot_min, plot_max, 100)],
        },
    })
