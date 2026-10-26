#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import numpy
from sklearn.manifold import MDS

def run(input: str) -> str:
    j = json.loads(input)
    mds = MDS(n_init=5, n_components=2)     # fit MDS model to data
    r = mds.fit_transform(numpy.array([[i[k] for k in j["group"]] for i in j["data"]]))
    z = [{"x": f"{i[0]:0.3f}", "y": f"{i[1]:0.3f}"} for i in zip(r[:, 0], r[:, 1])]
    d = [{i[0][j["label"][0]]: i[1]} for i in zip(j["data"], z)]
    s = {k: numpy.array([i[k] for i in j["data"]]) for k in j["group"]}

    return json.dumps({
        "table": {
            "thead": "<tr><th style='width: 40%;'>Variable</th><th style='width: 15%;'>Mean</th><th style='width: 15%;'>Variance</th><th style='width: 15%;'>Maximum</th><th>Minimum</th></tr>",
            "tbody": "".join([
                f"<tr><td>{a}</td><td>{b.mean():0.3f}</td><td>{b.var():0.3f}</td>" + 
                f"<td>{b.min():0.3f}</td><td>{b.max():0.3f}</td></tr>" for a, b in s.items()]),
        },
        "data": {k: [u[k] for u in d if k in u] for k in set([i[j["label"][0]] for i in j["data"]])},
    })
