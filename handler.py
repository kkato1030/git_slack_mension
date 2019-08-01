import json
import re

from urllib import request


# get mension list
with open('./config.json') as f:
    data = f.read()
    config = json.loads(data)
    mension_list = config['mension']
    webhook_url = config['webhook_url']


def main(event=None, context=None):
    print('[INFO]', 'event:', event)

    github_event = event['headers']['X-GitHub-Event']
    body = json.loads(event['body'])

    prefix = get_target_prefix(github_event, body['action'])
    html_url = body[prefix]['html_url']
    target_text = body[prefix]['body']
    print('[INFO]', 'target_text:', target_text)

    github_ids = get_github_ids(target_text)
    if not len(github_ids):
        return {
            'statusCode': 200,
            'body': 'pass through',
        }

    slack_ids = get_slack_ids(github_ids)
    if not len(slack_ids):
        return {
            'statusCode': 200,
            'body': 'pass through',
        }

    slack_mension = ' '.join(map(get_slack_mension, slack_ids))
    message = f"""{slack_mension}
You are mensioned in {github_event}.
{html_url}
"""
    print('[INFO]', 'message:', message)
    send_slack(message)

    return {
        'statusCode': 200,
        'body': 'send to slack.',
    }


def get_github_ids(text):
    """
    Githubのidリストをtextから取得する

    Parameters
    ----------
    text : string
        idを取得するリスト

    Returns
    -------
    github_ids : list
        Githubのidリスト
    """
    regex = '@[A-Za-z0-9-/]+'

    return re.findall(regex, text)


def get_target_prefix(github_event, action):
    """
    文章やURLを取得するためのprefixを取得する

    Parameters
    ----------
    github_event : string
        Githubのイベント名
    action: string
        Githubのアクション名

    Returns
    -------
    prefix : string
        bodyから文章やURLを取得するためのprefix
    """
    if action in ('created', 'opened', 'edited'):
        if github_event == 'pull_request':
            return 'pull_request'

        if github_event == 'issues':
            return 'issue'

        if github_event in ('issue_comment', 'pull_request_review_comment'):
            return 'comment'

    return ''


def send_slack(message):
    """
    slack通知

    Parameters
    ----------
    message : string
        送信文面

    Returns
    -------
    """
    url = webhook_url
    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }
    method = 'POST'
    data = {
        'username': 'gitslack',
        'text': message,
        'icon_emoji': ':octocat'
    }
    json_data = json.dumps(data).encode('utf-8')
    req = request.Request(
        url=url,
        data=json_data,
        headers=headers,
        method=method
    )
    request.urlopen(req, timeout=5)


def get_slack_ids(github_ids):
    slack_ids = []
    for github_id in github_ids:
        slack_id = mension_list.get(github_id)
        if slack_id is None:
            continue

        slack_ids.append(slack_id)

    return slack_ids


def get_slack_mension(slack_id):
    return f'<@{slack_id}>'


if __name__ == '__main__':
    main()
