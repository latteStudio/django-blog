from fabric import task, Connection
from invoke import Responder
from credentials import github_username, github_password


def delpoy():
    c = Connection(host='192.168.80.200', user='blog')
    c.run('pwd')

delpoy()
# def _get_github_auth_responders():
#     username_responder = Responder(
#         pattern="Username for 'https//github.com':",
#         response='{}\n'.format(github_username)
#     )
#
#     password_responder = Responder(
#         pattern="Password for 'https://{}@github.com':".format(github_username),
#         response = '{}\n'.format(github_password)
#     )
#
#     return [username_responder, password_responder]
#
#
# @task()
# def deploy(c):
#     conn = connection
#     supervisor_conf_path = '~/etc'
#     supervisor_program_name = 'django-blog'
#
#     project_root_path = '~/django-blog/'
#
# # 先停止应用
#     with c.cd(supervisor_conf_path):
#         cmd = 'supervisorctl stop {}'.format(supervisor_program_name)
#         c.run(cmd)
#
# # 进入项目根目录，git拉取最新代码
#     with c.cd(project_root_path):
#         cmd = 'git pull'
#         responders = _get_github_auth_responders()
#         c.run(cmd, watchers=responders)
#
# # 安装依赖、迁移数据库、收集静态文件
#     with c.cd(project_root_path):
#         c.run('pipenv install --deploy --ignore-pipfile')
#         c.run('pipenv run python manage.py migrate')
#         c,run('pipenv run python manage.py collectstatic --noinput')
#
# # 重新启动应用
#     with c.cd(supervisor_conf_path):
#         cmd = 'supervisorctl start {}'.format(supervisor_program_name)
#         c.run(cmd)
#

