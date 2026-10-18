import json
import numpy
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def run(input):
    j = json.loads(input)

    x = StandardScaler().fit_transform([[i[k] for k in j["group"]] for i in j["data"]])
    pca = PCA(n_components = 2)
    r = pca.fit_transform(x)

    z = [{"x": f"{i[0]:0.4f}", "y": f"{i[1]:0.4f}"} for i in zip(r[:, 0], r[:, 1])]
    s = {k: numpy.array([i[k] for i in j["data"]]) for k in j["group"]}
    d = [{i[0][j["label"][0]]: i[1]} for i in zip(j["data"], z)]

    return json.dumps({
        "table": {
            "thead": "<tr><th>Variable</th><th>Mean</th><th>Variance</th><th>Minimum</th><th>Maximum</th></tr>",
            "tbody": "".join([
                f"<tr><td>{a}</td><td>{b.mean():0.4f}</td><td>{b.var():0.4f}</td>" + 
                f"<td>{b.min():0.4f}</td><td>{b.max():0.4f}</td></tr>" for a, b in s.items()]),
        },
        "pca": [f"{i * 100:0.2f}" for i in pca.explained_variance_ratio_],
        "data": {k: [u[k] for u in d if k in u] for k in set([i[j["label"][0]] for i in j["data"]])},
    })
