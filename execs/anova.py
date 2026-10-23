#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import numpy
from scipy import stats

def run(input: str) -> str:
    """ main procedure begin here """
    j = json.loads(input)
    s = [[float(i[k]) for i in j["data"]] for k in j["g"]]
    f, p = stats.f_oneway(*s)   # variable length parameter

    tm = numpy.mean([b for a in s for b in a])                  # total mean
    sst = numpy.sum([pow(tm - b, 2) for a in s for b in a])     # sum of squares total
    ssw = numpy.sum([pow(b - numpy.mean(a), 2) for a in s for b in a])  # sum of squares within group

    r = {
        "between_ss": f"{(sst - ssw):0.4f}",
        "within_ss": f"{ssw:0.4f}",
        "between_df": len(j["g"]) - 1,
        "total_df": len(j["g"]) * len(s[0]) - 1,
    }   # calculate summary statistics and collect data

    r["within_df"] = r["total_df"] - r["between_df"]
    r["between_ms"] = f"{(float(r['between_ss']) / float(r['between_df'])):0.4f}"
    r["within_ms"] = f"{(float(r['within_ss']) / float(r['within_df'])):0.4f}"
    r["table"] = {
        "summary": {
            "thead": "<tr><th>Group</th><th>Mean</th><th>Variance</th><th>Maximum</th><th>Minimum</th></tr>",
            "tbody": "".join([
                f"<tr><td>{j['g'][i]}</td><td>{numpy.mean(s[i]):0.4f}</td><td>{numpy.var(s[i]):0.4f}</td>" +
                f"<td>{numpy.max(s[i]):0.4f}</td><td>{numpy.min(s[i]):0.4f}</td></tr>" for i in range(0, len(j["g"]))]),
        },
        "analysis": {
            "thead": "<tr><th>S. Variation</th><th>S.S.</th><th>D.F.</th><th>M.S.E.</th><th><i>F</i> Statistics</th><th><i>p</i> Value</th><tr>",
            "tbody": f"<tr><td>Between Group</td><td>{(sst - ssw):0.4f}</td><td>{len(j['g']) - 1}</td><td>{r['between_ms']}</td><td>{f:0.4f}</td><td>{p:0.4f}</td></tr>" + \
                f"<tr><td>Within Group</td><td>{ssw:0.4f}</td><td>{r['within_df']}</td><td>{r['within_ms']}</td><td>&nbsp;</td><td>&nbsp;</td></tr>" + \
                f"<tr><td>Total</td><td>{sst:0.4f}</td><td>{len(j['g']) * len(s[0]) - 1}</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>",
        }
    }

    return json.dumps({
        "table": r["table"],
        "data": {k: [float(i[k]) for i in j["data"]] for k in j["g"]},
    })
