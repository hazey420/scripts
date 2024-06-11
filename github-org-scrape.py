#!/usr/bin/env python3
import argparse
from bs4 import BeautifulSoup
import itertools
import json
import logging
import os
from pathlib import Path
import re
import requests
from subprocess import Popen, PIPE
import sys


SITE='https://github.com'
environment_variables = {}
global log_name, logger # accessible globally after setup_logging()

def run(cmd, stdin=None, binary=False):
    '''TODO: Log output as it is generated instead of returning it all at once'''
    if isinstance(cmd, str):
        cmd = cmd.split()
    lines = ''

    logger.debug(f'{Path.cwd()=} RUN: {" ".join(cmd)}')
    logger.debug(f'RUN: {" ".join(cmd)}')
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, env=environment_variables)
    if stdin:
        process.stdin.write(stdin.encode())
    stdout, stderr = process.communicate()
    logger.debug(f'OUTPUT: {stdout=}')
    logger.debug(f'ERROR: {stderr=}')
    if not binary:
        return stdout.decode()
    return stdout


def pull_branches(args):
    if not args.branches:
        return
    branch_names = []
    cur_branch = None
    try:
        for branch in run('git branch -a').splitlines():
            if branch.startswith('*'):
                branch = cur_branch = branch.replace('*', '').strip()
            branch = branch.strip()
            match = re.search(r"remotes/.+/(.+)", branch)
            if match:
                branch_names.append(match.group(1))
            else:
                branch_names.append(branch)
        if len(args.branches) == 1 and args.branches[0] == 'all':
            return branch_names
        for branch in list(set(args.branches) & set(branch_names)):
            run(f'git checkout {branch}')
    finally:
        if cur_branch:
            # restore branch it was on
            run(f'git checkout {cur_branch}')


def get_repos_from_json(data, org_name):
    hrefs = []
    repos = data['payload']['repositories']
    logger.debug(f'{repos=}')
    for repo in repos:
        hrefs.append(f'{org_name}/{repo["name"]}')
    return hrefs


def pull_org(org_name, get_all=False):
    site = f'{SITE}/orgs/{org_name}/repositories'
    logger.debug(f'Requesting {site=}')
    response = requests.get(site)
    if response.status_code != 200:
        #logger.info(f'Error getting {site=}, {response.status_code=}')
        site = f'{SITE}/{org_name}?tab=repositories'
        response = requests.get(site)
        if response.status_code != 200:
            return f'Error getting {site=}, {response.status_code=}'
    soup = BeautifulSoup(response.content, "html.parser")
    try:
        data = json.loads(f'{soup}')
        return get_repos_from_json(data, org_name)
    except:
        pass
    not_repos = ('/', 'forks', 'stargazers', 'issues', 'pulls', org_name)
    hrefs = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith(f'/{org_name}'):
            if not get_all and (href.endswith(not_repos) or '?' in Path(href).name):
                continue
            hrefs.append(href)
    return hrefs


def setup_logging(args):
    global log_name
    log_name = f'clone-{args.org}' if args.clone_org else f'update-{args.org}'
    log_name = f"{log_name.replace('/', '_').replace('.', '-')}.log"
    log_name = Path(log_name).absolute()
    # Create a custom logging format
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    # Create a file handler that logs DEBUG messages to logfile.log
    file_handler = logging.FileHandler(log_name)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Create a console handler that logs INFO messages to the console
    info_formatter = logging.Formatter("%(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(info_formatter)
    console_handler.setLevel(logging.INFO)

    # Create a logger with the specified handlers and set the log level to DEBUG
    logger = logging.getLogger(args.org)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


def _get_org(args):
    hrefs = pull_org(args.org)
    if not hrefs:
        return False, f"No repos found for {args.org=}, {hrefs=}"
    if isinstance(hrefs, str):
        return False, f"Error accessing org name {args.org}\n{hrefs}"
    return True, hrefs


def get_org(args):
    status, hrefs = _get_org(args)
    if status and hrefs:
        return hrefs
    if not status or not hrefs:
        logger.info(f'{status=}, {hrefs=}')
    if '/' in args.org:
        return [args.org]


def git_clone(args):
    hrefs = get_org(args)
    if not hrefs:
        return 1
    [logger.info(h) for h in hrefs]
    yesno = input('Clone? y/N: ')
    if yesno.lower() not in ('y', 'yes'):
        logger.info('Not cloned')
        return 0
    run(f'mkdir -p {args.org}')
    curdir = os.getcwd()
    if '/' not in args.org:
        os.chdir(args.org)
    for repo in hrefs:
        logger.info(f'##### Cloning repo {repo}')
        run(f'git clone {SITE}/{repo}.git')
        pull_branches(args)
    os.chdir(curdir)


def _find_repos(path):
    git_repos = []
    for entry in path.iterdir():
        if entry.is_dir():
            if entry.name == '.git':
                git_repos.append(entry.parent.absolute())
            else:
                git_repos.extend(_find_repos(entry))
    return git_repos


def git_update(args):
    directory = Path(args.org)
    assert directory.is_dir(), '--update expects a directory'
    logger.info(f'Looking for all repos in "{directory}"')
    repos = _find_repos(directory)
    for repo in repos:
        curdir = Path.cwd()
        try:
            logger.info(f'Updating {repo.relative_to(Path.cwd())}')
            os.chdir(repo.absolute())
            run('git pull --recurse-submodules')
            pull_branches(args)
        except:
            logger.info(f'Error pulling {repo}')
        finally:
            os.chdir(curdir)


def main(args):
    logger.debug(f'##### NEW RUN #####')
    try:
        if args.clone_org:
            git_clone(args)
        else:
            git_update(args)
    finally:
        os.chdir(args.orig_cwd)
        logger.info(f'Log is at "{log_name}"')
    return 0


if __name__=="__main__":
    parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('org', help='The repo org to clone or update', action='store')
    parser.add_argument('-c', '--clone-org', action='store_true', help='Clone the org (default)')
    parser.add_argument('-u', '--update-org', action='store_true',
            help='Update specified repo or all repos in given directory'
    )
    parser.add_argument('-b', '--branches', nargs='+', action='append',
            help='Get these branches (or "all")')
    args = parser.parse_args()
    if not args.clone_org and not args.update_org:
        # default to cloning
        args.clone_org = True
    if args.branches:
        args.branches = list(itertools.chain(*args.branches))
    args.orig_cwd = Path.cwd()
    if '/' in args.org:
        parent = Path(args.org).parent
        parent.mkdir(exist_ok=True)
    elif args.org == '.':
        args.org = Path(args.org).absolute().name
        os.chdir('..')
    logger = setup_logging(args)
    sys.exit(main(args))
