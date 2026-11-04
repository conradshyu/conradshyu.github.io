#!/usr/bin/env python
# -*- coding: utf-8 -*-

import html
import json

import numpy
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage


def run(input: str) -> str:
    j = json.loads(input)
    rows = j["data"]
    features = j["features"]

    if len(rows) < 2:
        raise ValueError("Ward clustering requires at least two observations.")
    if not features:
        raise ValueError("Select at least one numerical measurement variable.")

    try:
        matrix = numpy.asarray(
            [[row[feature] for feature in features] for row in rows],
            dtype=float,
        )
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("Selected measurement variables must contain numeric values.") from error

    if not numpy.isfinite(matrix).all():
        raise ValueError("Selected measurement variables must not contain missing or infinite values.")

    cluster_count = int(j["clusters"])
    if cluster_count < 1 or cluster_count > len(rows):
        raise ValueError("The number of clusters must be between 1 and the number of observations.")

    tree = linkage(matrix, method="ward")
    if cluster_count == 1:
        cut_distance = float(tree[-1, 2]) + max(1.0, float(tree[-1, 2]) * 0.01)
    elif cluster_count == len(rows):
        cut_distance = 0.0
    else:
        lower_merge = tree[len(rows) - cluster_count - 1, 2]
        upper_merge = tree[len(rows) - cluster_count, 2]
        cut_distance = float((lower_merge + upper_merge) / 2)

    assignments = fcluster(tree, cluster_count, criterion="maxclust")
    label_fields = j.get("label", [])
    observation_labels = []
    for index, row in enumerate(rows):
        label = row[label_fields[0]] if label_fields else f"Observation {index + 1}"
        observation_labels.append(str(label) or f"Observation {index + 1}")

    tree_data = dendrogram(
        tree,
        labels=observation_labels,
        no_plot=True,
        color_threshold=cut_distance,
        above_threshold_color="#64748b",
    )
    palette = {
        "C0": "#1f77b4",
        "C1": "#ff7f0e",
        "C2": "#2ca02c",
        "C3": "#d62728",
        "C4": "#9467bd",
        "C5": "#8c564b",
        "C6": "#e377c2",
        "C7": "#7f7f7f",
        "C8": "#bcbd22",
        "C9": "#17becf",
    }

    branches = []
    for x_values, y_values, color in zip(
        tree_data["icoord"], tree_data["dcoord"], tree_data["color_list"]
    ):
        branches.append({
            "color": palette.get(color, "#64748b"),
            "data": [
                {"x": (float(x) - 5) / 10, "y": float(y)}
                for x, y in zip(x_values, y_values)
            ],
        })

    cluster_ids = sorted(set(int(value) for value in assignments))
    table_rows = []
    for cluster_id in cluster_ids:
        cluster_data = matrix[assignments == cluster_id]
        means = "".join(
            f"<td>{cluster_data[:, index].mean():0.3f}</td>"
            for index in range(len(features))
        )
        table_rows.append(
            f"<tr><td>Cluster {cluster_id}</td><td>{len(cluster_data)}</td>{means}</tr>"
        )

    feature_headers = "".join(
        f"<th>{html.escape(str(feature))} Mean</th>" for feature in features
    )
    return json.dumps({
        "table": {
            "thead": (
                "<tr><th>Cluster</th><th>Observations</th>"
                f"{feature_headers}</tr>"
            ),
            "tbody": "".join(table_rows),
        },
        "dendrogram": {
            "labels": [str(label) for label in tree_data["ivl"]],
            "branches": branches,
            "cut_distance": cut_distance,
        },
    })
