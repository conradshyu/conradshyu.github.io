import json
import numpy
from sklearn.manifold import MDS

def run(input):
    j = json.loads(input)
    mds = MDS(n_init=5, n_components=2)     # fit MDS model to data
    r = mds.fit_transform(numpy.array([[i[k] for k in j["group"]] for i in j["data"]]))
    z = [{"x": f"{i[0]:0.4f}", "y": f"{i[1]:0.4f}"} for i in zip(r[:, 0], r[:, 1])]
    d = [{i[0][j["label"][0]]: i[1]} for i in zip(j["data"], z)]
    s = {k: numpy.array([i[k] for i in j["data"]]) for k in j["group"]}

    return json.dumps({
        "table": {
            "thead": "<tr><th>Variable</th><th>Mean</th><th>Variance</th><th>Minimum</th><th>Maximum</th></tr>",
            "tbody": "".join([
                f"<tr><td>{a}</td><td>{b.mean():0.4f}</td><td>{b.var():0.4f}</td>" + 
                f"<td>{b.min():0.4f}</td><td>{b.max():0.4f}</td></tr>" for a, b in s.items()]),
        },
        "data": {k: [u[k] for u in d if k in u] for k in set([i[j["label"][0]] for i in j["data"]])},
    })
