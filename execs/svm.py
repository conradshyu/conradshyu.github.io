#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
import numpy
import pandas
import argparse
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, accuracy_score

def main(argv):
    """ main procedure begin here """
    #s = pandas.read_json(argv.input).sample(n = 5000)
    s = pandas.read_json(argv.input)
    x_train, x_test, y_train, y_test = train_test_split(
        s[argv.x], s[argv.y], test_size = 0.25, random_state = 17)

    r = SVC(kernel = "linear", random_state = 17)
    r.fit(x_train, y_train)
    p = r.predict(x_test)
    j = json.load(open(argv.input, "r"))

    print(json.dumps({
        "table": {
            "thead": "<tr><th>Variable</th><th>Min</th><th>Max</th><th>Mean</th><th>Variance</th></tr>",
            "tbody": "".join([f"<tr><td>{a}</td>" + \
                f"<td>{b.min():0.2f}</td><td>{b.max():0.2f}</td><td>{b.mean():0.2f}</td><td>{b.var():0.2f}</td></tr>" \
                for a, b in ({i: numpy.array([d[i] for d in j]) for i in argv.x}).items()]),
        },
        "error": [
            f"{mean_absolute_error(y_test, p):0.2f}",
            f"{mean_squared_error(y_test, p):0.2f}",
            f"{r2_score(y_test, p):0.2f}",
            f"{accuracy_score(y_test, p):0.2f}",
        ],
        "data": {
            "observed": [{"x": i[0], "y": i[1]} for i in zip(x_test[argv.x[0]], y_test)],
            "predicted": [{"x": i[0], "y": i[1]} for i in zip(x_test[argv.x[0]], p)],
        },
    }))

    return True

if __name__ == "__main__":
    argv = argparse.ArgumentParser(description = """
        Multivariate Analysis of Variance (MANOVA)""",
        formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    argv.add_argument("--input", "-i", type = str, required = True,
        help = "[Required] Input JSON file.", dest = "input")
    argv.add_argument("--x", "-x", type = str, nargs = '+', default = [], required = True,
        help = "[Required] Predictor variables(s).", dest = "x")
    argv.add_argument("--y", "-y", type = str, default = "", required = True,
        help = "[Required] Response variable.", dest = "y")

    sys.exit(not main(argv.parse_args()))
