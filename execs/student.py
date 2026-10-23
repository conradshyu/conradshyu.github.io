#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import numpy
from scipy import stats

"""
A t-test may be used to evaluate whether a single group differs from a known value (a one-sample t-test),
whether two groups differ from each other (an independent two-sample t-test), or whether there is a
significant difference in paired measurements (a paired, or dependent samples t-test).
"""
class Student:
    def __init__(self, input):
        self.z = [[float(i[k]) for i in input["data"]] for k in input["g"]]
        self.t = input["g"]

    def single(self):
        """ one sample t-test """
        s = stats.ttest_1samp(numpy.array(self.z[0]), popmean = 0.0)

        x = numpy.linspace(
            min(self.z[0]) if min(self.z[0]) < -4.0 else -4.0,
            max(self.z[0]) if max(self.z[0]) > 4.0 else 4.0, 100)
        t1 = stats.t.pdf(
            x, df = len(self.z[0]) - 1, loc = 0.0, scale = 1.0)
        t2 = stats.t.pdf(
            self.z[0], df = len(self.z[0]) - 1, loc = numpy.array(self.z[0]).mean(),
            scale = numpy.array(self.z[0]).std())

        return json.dumps({
            "table": [{
                "thead": "<tr><th>Variable</th><th>Mean</th><th>Variance</th><th>Minimum</th><th>Maximum</th></tr>",
                "tbody": f"<tr><td>{self.t[0]}</td><td>{numpy.array(self.z[0]).mean():0.4f}</td>" + 
                    f"<td>{numpy.array(self.z[0]).var():0.4f}</td><td>{min(self.z[0]):0.4f}</td><td>{max(self.z[0]):0.4f}</td></tr>",
            }, {
                "thead": "<tr><th>Description</th><th>Value</th></tr>",
                "tbody": f"<tr><td><i>t</i> Statistics</td><td>{s.statistic:0.4f}</td></tr>" +
                    f"<tr><td><i>p</i> Value</td><td>{s.pvalue:0.4f}</td></tr>" +
                    f"<tr><td>Upper Critical <i>t</i> Value</td><td>{stats.t.ppf(1.0 - 0.95 * 0.5, len(self.z[0]) - 1):0.4f}</td></tr>" +
                    f"<tr><td>Lower Critical <i>t</i> Value</td><td>{stats.t.ppf(0.05 * 0.5, len(self.z[0]) - 1):0.4f}</td></tr>" +
                    f"<tr><td>One-Tail Upper Critical <i>t</i> Value</td><td>{stats.t.ppf(0.95, len(self.z[0]) - 1):0.4f}</td></tr>",
            }],
            "data": {
                "standard": [{"x": i[0], "y": i[1]} for i in zip(x, t1)],
                "observed": [{"x": i[0], "y": i[1]} for i in zip(self.z[0], t2)],
            }
        })


    def double(self):
        """ two independent t-test """
        s = stats.ttest_ind(numpy.array(self.z[0]), numpy.array(self.z[1]))

        """
        x = numpy.linspace(
            min(self.z[0]) if min(self.z[0]) < -4.0 else -4.0,
            max(self.z[0]) if max(self.z[0]) > 4.0 else 4.0, 100)
        """
        x = numpy.linspace(-4.0, 4.0, 100)
        t0 = stats.t.pdf(
            x, df = len(self.z[0]) - 1, loc = 0.0, scale = 1.0)
        t1 = stats.t.pdf(
            self.z[0], df = len(self.z[0]) - 1, loc = numpy.array(self.z[0]).mean(),
            scale = numpy.array(self.z[0]).std())
        t2 = stats.t.pdf(
            self.z[1], df = len(self.z[1]) - 1, loc = numpy.array(self.z[1]).mean(),
            scale = numpy.array(self.z[1]).std())

        return json.dumps({
            "table": [{
                "thead": "<tr><th>Variable</th><th>Mean</th><th>Variance</th><th>Minimum</th><th>Maximum</th></tr>",
                "tbody": f"<tr><td>{self.t[0]}</td><td>{numpy.array(self.z[0]).mean():0.4f}</td>" + 
                    f"<td>{numpy.array(self.z[0]).var():0.4f}</td><td>{min(self.z[0]):0.4f}</td><td>{max(self.z[0]):0.4f}</td></tr>" +
                    f"<tr><td>{self.t[1]}</td><td>{numpy.array(self.z[1]).mean():0.4f}</td>" +
                    f"<td>{numpy.array(self.z[1]).var():0.4f}</td><td>{min(self.z[1]):0.4f}</td><td>{max(self.z[1]):0.4f}</td></tr>",
            }, {
                "thead": "<tr><th>Description</th><th>Value</th></tr>",
                "tbody": f"<tr><td><i>t</i> Statistics</td><td>{s.statistic:0.4f}</td></tr>" +
                    f"<tr><td><i>p</i> Value</td><td>{s.pvalue:0.4f}</td></tr>",
            }],
            "data": {
                "standard": [{"x": i[0], "y": i[1]} for i in zip(x, t0)],
                self.t[0]: [{"x": i[0], "y": i[1]} for i in zip(self.z[0], t1)],
                self.t[1]: [{"x": i[0], "y": i[1]} for i in zip(self.z[1], t2)],
            }
        })

    def paired(self):
        """ paired sample t-test """
        s = stats.ttest_rel(numpy.array(self.z[0]), numpy.array(self.z[1]))
        w = [i[0] - i[1] for i in zip(self.z[0], self.z[1])]

        x = numpy.linspace(-4.0, 4.0, 100)
        t0 = stats.t.pdf(
            x, df = len(self.z[0]) - 1, loc = 0.0, scale = 1.0)
        t1 = stats.t.pdf(
            w, df = len(w) - 1, loc = numpy.array(w).mean(),
            scale = numpy.array(w).std())
        t2 = stats.t.pdf(
            self.z[0], df = len(self.z[0]) - 1, loc = numpy.array(self.z[0]).mean(),
            scale = numpy.array(self.z[0]).std())
        t3 = stats.t.pdf(
            self.z[1], df = len(self.z[1]) - 1, loc = numpy.array(self.z[1]).mean(),
            scale = numpy.array(self.z[1]).std())

        return json.dumps({
            "table": [{
                "thead": "<tr><th>Variable</th><th>Mean</th><th>Variance</th><th>Minimum</th><th>Maximum</th></tr>",
                "tbody": f"<tr><td>{self.t[0]}</td><td>{numpy.array(self.z[0]).mean():0.4f}</td>" + 
                    f"<td>{numpy.array(self.z[0]).var():0.4f}</td><td>{min(self.z[0]):0.4f}</td><td>{max(self.z[0]):0.4f}</td></tr>" +
                    f"<tr><td>{self.t[1]}</td><td>{numpy.array(self.z[1]).mean():0.4f}</td>" +
                    f"<td>{numpy.array(self.z[1]).var():0.4f}</td><td>{min(self.z[1]):0.4f}</td><td>{max(self.z[1]):0.4f}</td></tr>",
            }, {
                "thead": "<tr><th>Description</th><th>Value</th></tr>",
                "tbody": f"<tr><td><i>t</i> Statistics</td><td>{s.statistic:0.4f}</td></tr>" +
                    f"<tr><td><i>p</i> Value</td><td>{s.pvalue:0.4f}</td></tr>",
            }],
            "data": {
                "paired": [{"x": i[0], "y": i[1]} for i in zip(w, t1)],
                "standard": [{"x": i[0], "y": i[1]} for i in zip(x, t0)],
                self.t[0]: [{"x": i[0], "y": i[1]} for i in zip(self.z[0], t2)],
                self.t[1]: [{"x": i[0], "y": i[1]} for i in zip(self.z[1], t3)],
            }
        })

def main(input):
    """ main procedure """
    j = json.loads(input)
    s = Student(j)
    run = {
        "single": lambda: s.single(),
        "double": lambda: s.double(),
        "paired": lambda: s.paired(),}

    return run[j["t"]]()
