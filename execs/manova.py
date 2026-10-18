import json
import pandas
from statsmodels.multivariate.manova import MANOVA

MANOVA_TH = ["Value", "Num DF", "Den DF", "<i>F</i> Statistic", "<i>p</i> Value"]
MANOVA_TR = ["Wilks' Lambda", "Pillai's Trace", "Hotelling-Lawley Trace", "Roy's Greatest Root"]
MANOVA_TD = ["Value","Num DF", "Den DF", "F Value", "Pr > F"]

def html_table(h, s):
    """ generate manova table """
    return {
        "thead": f"<tr><th>{h}</th>" + "".join([f"<th>{i}</th>" for i in MANOVA_TH]) + "</tr>",
        "tbody": "".join([f"<tr><td>{MANOVA_TR[i]}</td>" + "".join([f"<td>{s[i][j]:0.2f}</td>" for j in MANOVA_TD]) \
            + "</tr>" for i in range(len(s))]),}

def run(input):
    """ main procedure begin here """
    j = json.loads(input)
    s = {j["x"][0]: [i[j["x"][0]] for i in j["data"]]}
    s.update({k: [float(i[k]) for i in j["data"]] for k in j["y"]})

    # run manova using a formula
    r = MANOVA.from_formula(f"{' + '.join([i for i in j['y']])} ~ {j['x'][0]}", data = s)
    t = json.loads(pandas.DataFrame(r.mv_test().results).to_json(orient = "records"))

    return json.dumps({
        "table": [
            html_table("Intercept", t[0]["Intercept"]),     # intercept table
            html_table(j["x"][0], t[0][j["x"][0]]),],      # group table
        "data": {k: [float(i[k]) for i in j["data"]] for k in j["y"]},})
