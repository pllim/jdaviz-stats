"""Get a list of open GitHub issues and save them to a file.

This is an expensive operation. Further processing can be done separately
using the output file.

"""
import os
from datetime import datetime

from github import Github

__all__ = ['get_open_issues']


def get_open_issues(reponame='spacetelescope/jdaviz',
                    filename_prefix='jdaviz_open_issues', overwrite=False,
                    verbose=True):
    """Query GitHub for open issues for the given ``reponame`` and save the
    results as CSV with ``filename_prefix``.

    """
    try:
        token = os.environ['GITHUB_TOKEN']
    except KeyError:
        raise KeyError('GITHUB_TOKEN environment variable is not set') from None  # noqa

    today = datetime.today()
    tformat = '%Y-%m-%dT%H:%M:%SZ'
    filename = f'{filename_prefix}_{today.strftime(tformat)}.csv'

    # Highly unlikely with timestamp but you never know.
    if os.path.exists(filename) and not overwrite:
        raise OSError(f'{filename} exists')

    g = Github(token)
    repo = g.get_repo(reponame)
    open_issues = repo.get_issues(state='open')
    rows = [('number', 'created_at', 'type', 'creator', 'assignee', 'labels',
             'lifetime_seconds')]

    for issue in open_issues:
        lifetime = (today - issue.created_at).total_seconds()

        if issue.pull_request is None:
            issue_type = 'issue'
        else:
            issue_type = 'pull_request'

        if issue.assignee is None:
            assignee = ''
        else:
            assignee = issue.assignee.login

        issue_labels = ','.join([lbl.name for lbl in issue.labels])

        rows.append([str(issue.number), issue.created_at.strftime(tformat),
                     issue_type, issue.user.login, assignee,
                     f'"{issue_labels}"', str(lifetime)])

    with open(filename, 'w') as fout:
        for row in rows:
            fout.write(f"{','.join(row)}{os.linesep}")

    if verbose:
        print(f'{filename} written')


if __name__ == '__main__':
    get_open_issues()
