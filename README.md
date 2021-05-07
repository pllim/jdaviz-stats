# jdaviz-stats

Scripts to generate GitHub stats for [Jdaviz](https://github.com/spacetelescope/jdaviz).

## Requires

* Python 3.6 or later
* bokeh
* numpy
* pandas
* pygithub

## Instructions

1. Set your `GITHUB_TOKEN` environment variable.

2. Run `scripts/get_stats.py` to obtain `jdaviz_open_issues_<timestamp>.csv`
   in your working directory.

3. Run `scripts/histogram_by_label_bokeh.py` to generate a
   `histogram_by_label_bokeh.html` file.

4. Serve your HTML file to share the interactive plot.

5. If you want to save the outputs, remember to move them outside of this
   repository so you do not accidentally delete them when you run `git clean`.
