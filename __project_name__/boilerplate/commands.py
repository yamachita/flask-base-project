import os
from pathlib import Path

import click


@click.command()
@click.option('--bare', is_flag=True, default=False)
@click.argument('api_name')
def create_api(api_name: str, bare):

    project_name = os.environ.get('PROJECT_NAME')

    if not project_name:
        print('É necessário setar a variável de ambiente PROJECT_NAME')
        return

    cwd_dirs_name = [path.name for path in os.listdir(Path.cwd())]

    if '__project_name__' in cwd_dirs_name:
        print(
            'É necessário executar o comando "flask init-project <project name>" primeiro.')
        return

    api_dir = Path.cwd() / project_name / api_name
    api_dir.mkdir()

    file_names = ['models', 'schemas', 'services', 'controllers', 'routes']

    for name in file_names:
        dir_path = api_dir/f'{name}.py'
        dir_path.touch()

    if bare == False:

        model_class = api_name.capitalize()
        model_name = api_name

        api_tpl_dir = Path.cwd() / project_name / 'boilerplate' / 'api_templates'

        for name in file_names:
            dir_path_py = api_dir/f'{name}.py'
            dir_path_tpl = api_tpl_dir/f'{name}.py-tpl'
            template_data = dir_path_tpl.read_text()

            _create_bp(file_path=dir_path_py,
                       data=template_data,
                       project_name=project_name,
                       model_class=model_class,
                       model_name=model_name)


@click.command()
@click.argument('project_name')
def init_project(project_name):

    name = project_name

    if project_name is None:
        name = os.environ.get('PROJECT_NAME')
        if name is None or name == '__project_name__':
            print('É necessário definir um nome para o projeto.')
            print(
                'Você pode definir passando como argumento: flask init-project <project_name>')
            print('Você também pode definir setando a variável de ambiente PROJECT_NAME')
            return
    else:
        os.environ['PROJECT_NAME'] = name

    env_path = Path.cwd() / '.env'
    data = env_path.read_text()
    data = data.replace('__project_name__', name)
    env_path.write_text(data)

    path_dir = Path.cwd() / '__project_name__'
    user_dir = path_dir / 'user'
    auth_dir = path_dir / 'auth'
    storage_dir = path_dir / 'storage'

    file_names = ['services.py', 'models.py', 'extensions.py'
                  'app.py', 'utils/filters.py', 'utils/mail.py']

    for name in file_names:
        path = path_dir / name
        data = path.read_text()
        data = data.replace('__project_name__', name)
        path.write_text(data)

    path_iter_dir = [user_dir, auth_dir, storage_dir]

    for iter_dir in path_iter_dir:
        for path in iter_dir.iterdir():
            data = path.read_text()
            data = data.replace('__project_name__', name)
            path.write_text(data)

    new_path_dir = Path.cwd() / name

    path_dir.rename(new_path_dir)


def _create_bp(file_path: Path, data: str, **kwargs) -> None:

    replace_dict = {'{{'+k+'}}': v for k, v in kwargs.items()}

    for k, v in replace_dict.items():
        data = data.replace(k, v)

    file_path.write_text(data)
