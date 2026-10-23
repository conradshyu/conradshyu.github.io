#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import numpy
import pandas
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, accuracy_score

def run(input: str) -> str:
    """ main procedure begin here """
    u = json.loads(input)
    s = pandas.read_json(json.dumps(u["data"]))
    x_train, x_test, y_train, y_test = train_test_split(
        s[u["x"]], s[u["y"][0]], test_size = 0.25, random_state = 17)

    r = GaussianNB()    # gaussian naive bayes
    r.fit(x_train, y_train)
    p = r.predict(x_test)
    j = u["data"]

    return json.dumps({
        "table": {
            "thead": "<tr><th>Variable</th><th>Min</th><th>Max</th><th>Mean</th><th>Variance</th></tr>",
            "tbody": "".join([f"<tr><td>{a}</td>" + \
                f"<td>{b.min():0.2f}</td><td>{b.max():0.2f}</td><td>{b.mean():0.2f}</td><td>{b.var():0.2f}</td></tr>" \
                for a, b in ({i: numpy.array([d[i] for d in j]) for i in u["x"]}).items()]),
        },
        "error": [
            f"{mean_absolute_error(y_test, p):0.2f}",
            f"{mean_squared_error(y_test, p):0.2f}",
            f"{r2_score(y_test, p):0.2f}",
            f"{accuracy_score(y_test, p):0.2f}",
        ],
        "data": {
            "observed": [{"x": i[0], "y": int(i[1])} for i in zip(x_test[u["x"][0]], y_test)],
            "predicted": [{"x": i[0], "y": int(i[1])} for i in zip(x_test[u["x"][0]], p)],
        },
    })
