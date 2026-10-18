import json
import numpy
from sklearn import linear_model

def run(js):
    """ main procedure begin here """
    input = json.loads(js)
    j = sorted(input["data"], key = lambda i: i[input["y"][0]])
    x = [[float(i[k]) for k in input["x"]] for i in j]
    y = [[float(i[k]) for k in input["y"]] for i in j]

    r = linear_model.LinearRegression().fit(x, y)
    xi = [sum([r.coef_[0][k] * i[input["x"][k]] for k in range(len(input["x"]))]) for i in j]
    xs = {k: numpy.array([i[k] for i in j]) for k in input["x"]}
    intercept = r.intercept_.sum() if isinstance(r.intercept_, numpy.ndarray) else r.intercept_

    # coefficient of determination of prediction, R^2
    return json.dumps({
        "table": {
            "analysis": {
                "thead": "<tr><th>Variable</th><th>Value</th></tr>",
                "tbody": f"<tr><td>Intercept</td><td>{intercept:0.4f}</td></tr>" + \
                    "".join([f"<tr><td>{a}</td><td>{b:0.4f}</td></tr>" for a, b in zip(input["x"], r.coef_[0])]) + \
                    f"<tr><td>R<sup>2</sup> Score</td><td>{r.score(numpy.array(x), y):.4f}</td></tr>",
            },
            "summary": {
                "thead": "<tr><th>Variable</th><th>Mean</th><th>Variance</th><th>Maximum</th><th>Minimum</th></tr>",
                "tbody": "".join([
                    f"<tr><td>{a}</td><td>{b.mean():0.4f}</td><td>{b.var():0.4f}</td><td>{b.max():0.4f}</td><td>{b.min():0.4f}</td></tr>" \
                    for a, b in xs.items()]),
            },
        },
        "data": {
            "observe": [{
                "x": i[0] + intercept,
                "y": i[1][0]} for i in zip(xi, y)],
            "predict": [{
                "x": i + intercept,
                "y": i + intercept} for i in numpy.linspace(min(xi), max(xi), 100)],
        },
    })
