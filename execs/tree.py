#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import numpy
import pandas
import sklearn.metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

def run(input: str) -> str:
    """ main procedure begin here """
    u = json.loads(input)
    s = pandas.DataFrame(u["data"])
    y_label = list(set([str(i[u["y"][0]]) for i in u["data"]]))
    x_train, x_test, y_train, y_test = train_test_split(
        s[u["x"]], [y_label.index(i[u["y"][0]]) for i in s.to_dict(orient="records")],
        test_size = 0.25, random_state = 17)
    r = DecisionTreeClassifier()    # decision tree classifier
    r.fit(x_train, y_train)
    y_pred = r.predict(x_test)
    j = u["data"]

    return json.dumps({
        "table": {
            "thead": "<tr><th style='width: 40%;'>Variable</th><th style='width: 15%;'>Min</th><th style='width: 15%;'>Max</th><th style='width: 15%;'>Mean</th><th>Variance</th></tr>",
            "tbody": "".join([f"<tr><td>{a}</td>" + \
                f"<td>{b.min():0.3f}</td><td>{b.max():0.3f}</td><td>{b.mean():0.3f}</td><td>{b.var():0.3f}</td></tr>" \
                for a, b in ({i: numpy.array([d[i] for d in j]) for i in u["x"]}).items()]),
        },
        "error": {
            "thead": "<tr><th style='width: 60%;'>Metric Name</th><th>Value</th></tr>",
            "tbody": "".join([
                f"<tr><td>Accuracy</td><td>{sklearn.metrics.accuracy_score(y_test, y_pred):0.3f}</td></tr>",
                f"<tr><td>Balanced Accuracy</td><td>{sklearn.metrics.balanced_accuracy_score(y_test, y_pred, adjusted=True):0.3f}</td></tr>",
                f"<tr><td>Mean Absolute Error</td><td>{sklearn.metrics.mean_absolute_error(y_test, y_pred, multioutput='raw_values')[0]:0.3f}</td></tr>",
                f"<tr><td>Mean Squared Error</td><td>{sklearn.metrics.mean_squared_error(y_test, y_pred):0.3f}</td></tr>",
                f"<tr><td>Root Mean Squared Error</td><td>{sklearn.metrics.root_mean_squared_error(y_test, y_pred):0.3f}</td></tr>",
                f"<tr><td><em>R²</em></td><td>{sklearn.metrics.r2_score(y_test, y_pred):0.3f}</td></tr>",
            ]),
        },
        "feature": {
            "thead": "<tr><th style='width: 60%;'>Feature</th><th>Importance</th></tr>",
            "tbody": "".join([f"<tr><td>{a}</td><td>{b:0.3f}</td></tr>" for a, b in zip(u["x"], r.feature_importances_)])
        },
        "data": {
            "observed": [{"x": i[0], "y": int(i[1])} for i in zip(x_test[u["x"][0]], y_test)],
            "predicted": [{"x": i[0], "y": int(i[1])} for i in zip(x_test[u["x"][0]], y_pred)],
        },
    })
