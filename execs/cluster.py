#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import numpy
from sklearn.cluster import KMeans

def run(input: str) -> str:
    """ main procedure begin here """
    j = json.loads(input)
    x = [[i[k] for k in j["x"]] for i in j["data"]]
    y = set([i[j["y"][0]] for i in j["data"]])
    r = KMeans(n_clusters = len(y), random_state = 17, n_init = 'auto')
    r.fit(x)
    s = {k: {i: numpy.array([z[i] for z in j["data"] if z[j["y"][0]] == k]) for i in j["x"]} for k in y}

    d = {a: [{"x": float(v[0]), "y": float(v[1])} for v in zip(b[j["x"][0]], b[j["x"][1]])] \
        for a, b in s.items()}
    d.update({"centroid": [{"x": float(i[0]), "y": float(i[1])} \
        for i in zip(r.cluster_centers_[:, 0], r.cluster_centers_[:, 1])],})

    return json.dumps({
        "table": {
            a: {
                "thead": "<tr><th style='width: 40%;'>Variable</th><th style='width: 15%;'>Min</th><th style='width: 15%;'>Max</th><th style='width: 15%;'>Mean</th><th>Variance</th></tr>",
                "tbody": "".join([f"<tr><td>{k}</td><td>{v.min():0.2f}</td><td>{v.max():0.2f}</td>" + \
                    f"<td>{v.mean():0.2f}</td><td>{v.var():0.2f}</td></tr>" for k, v in b.items()]),
            } for a, b in s.items()
        },
        "data": d,
    })
