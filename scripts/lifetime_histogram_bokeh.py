"""Generates a Bokeh plot with issue stats vs certain labels.

This requires the CSV output file from ``get_stats.py`` and will generate a
HTML version with the same name as this file.

"""
# import math
from datetime import datetime

import numpy as np
import pandas as pd
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure, show

__all__ = ['do_plot']


def do_plot(stats_filename, labels=['cubeviz', 'embed', 'imviz', 'mosviz',
                                    'specviz', 'UI/UX']):
    tbl = pd.read_csv(stats_filename, parse_dates=['created_at'])
    tbl.fillna('', inplace=True)
    n_prs = []
    n_issues = []
    n_issues_bugs = []

    mask_pr = (tbl['type'] == 'pull_request').to_numpy(dtype=bool)
    mask_bug = tbl['labels'].str.contains('bug').to_numpy(dtype=bool)
    masks_not_in_labels = []

    for label in labels:
        mask = tbl['labels'].str.contains(label).to_numpy(dtype=bool)
        masks_not_in_labels.append(~mask)
        n_prs.append(len(tbl[mask & mask_pr]))
        n_issues.append(len(tbl[mask & ~mask_pr]))
        n_issues_bugs.append(len(tbl[mask & ~mask_pr & mask_bug]))

    # The Others
    mask = np.logical_and.reduce(masks_not_in_labels)
    labels.append('Others')
    n_prs.append(len(tbl[mask & mask_pr]))
    n_issues.append(len(tbl[mask & ~mask_pr]))
    n_issues_bugs.append(len(tbl[mask & ~mask_pr & mask_bug]))

    df = pd.DataFrame.from_dict({'labels': labels,
                                 'PRs': n_prs,
                                 'Issues_all': n_issues,
                                 'Issues_bug': n_issues_bugs})
    data = ColumnDataSource(df)
    TOOLTIPS = [
        ("Label", "@labels"),
        ("# Issues", "@Issues_all"),
        # ("# Issues (bug)", "@Issues_bug"),
        ("# PRs", "@PRs")]
    plot_title = ("Open issues/PRs by subpackage "
                  f"({datetime.today().strftime('%Y-%m-%d')}); "
                  "click on legend to show/hide")

    p = figure(title=plot_title, x_range=labels, plot_width=800,
               background_fill_color="#fafafa")
    g1 = p.vbar(x="labels", top="Issues_all", width=0.9, color="#9A44B6",
                source=data, legend_label="Issues (all)")
    g1_hover = HoverTool(renderers=[g1], tooltips=TOOLTIPS)
    # p.vbar(x="labels", top="Issues_bug", width=0.9, color="#A60628",
    #        fill_alpha=0.75, source=data, legend_label="Issues (bug)")
    p.vbar(x="labels", top="PRs", width=0.9, color="#338ADD", fill_alpha=0.5,
           source=data, legend_label="PRs")
    p.add_tools(g1_hover)

    p.y_range.start = 0
    p.yaxis.axis_label = '#'
    p.x_range.range_padding = 0.1
    # p.xaxis.major_label_orientation = math.pi / 2
    p.xaxis.major_label_text_font_size = "18pt"
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.legend.click_policy = "hide"
    p.legend.location = "top_left"

    show(p)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Generates a Bokeh plot with '
                                     'issue stats vs certain labels.')
    parser.add_argument('inputfile', type=str,
                        help='CSV file from get_stats.py')
    args = parser.parse_args()

    do_plot(args.inputfile)
