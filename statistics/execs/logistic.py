import json
import math
import numpy
from sklearn import linear_model

def run(input):
    """ main procedure begin here """
    s = json.loads(input)
    j = s["data"]
    x = [[float(i[k]) for k in s["x"]] for i in j]
    y = [i[s["y"][0]] for i in j]

    r = linear_model.LogisticRegression(random_state = 7).fit(x, y)
    xi = [r.intercept_[0] + sum([r.coef_[0][k] * i[s["x"][k]] for k in range(len(s["x"]))]) for i in j]
    mi = math.log(0.01 / 0.99) - r.intercept_[0]    # minimum range: p = 0.01
    mx = math.log(0.99 / 0.01) - r.intercept_[0]    # maximum range: p = 0.99
    xs = {k: numpy.array([i[k] for i in j]) for k in s["x"]}

    # coefficient of determination of prediction, goodness of fit
    return json.dumps({
        "table": {
            "analysis": {
                "thead": "<tr><th>Variable</th><th>Value</th></tr>",
                "tbody": f"<tr><td>Intercept</td><td>{r.intercept_[0]:0.4f}</td></tr>" + \
                    "".join([f"<tr><td>{a}</td><td>{b:0.4f}</td></tr>" for a, b in zip(s["x"], r.coef_[0])]) + \
                    f"<tr><td>Accuracy</td><td>{r.score(numpy.array(x), y):.4f}</td></tr>",
            },
            "summary": {
                "thead": "<tr><th>Variable</th><th>Mean</th><th>Variance</th><th>Maximum</th><th>Minimum</th></tr>",
                "tbody": "".join([
                    f"<tr><td>{a}</td><td>{b.mean():0.4f}</td><td>{b.var():0.4f}</td><td>{b.max():0.4f}</td><td>{b.min():0.4f}</td></tr>" \
                    for a, b in xs.items()]),
            },
        },
        "data": {
            "observe": [{"x": i[0], "y": i[1]} for i in zip(xi, y)],
            #"predict": [{"x": f"{i[0]:0.4f}", "y": i[1]} for i in zip(xi, r.predict(x).tolist())],
            "predict": [{
                "x": i,
                "y": 1.0 / (1 + math.exp(-1.0 * i))} for i in xi],
            "logit": [{
                "x": i + r.intercept_[0],
                "y": 1.0 / (1.0 + math.exp(-1.0 * (r.intercept_[0] + i)))} for i in numpy.linspace(mi, mx, 100)],
        },
    })
