import os
import random
import shutil
import string


try:
    # Inspired by
    # https://github.com/django/django/blob/master/django/utils/crypto.py
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False

PROJECT_DIR_PATH = os.path.realpath(os.path.curdir)


def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def remove_auto_createsuperuser_file():
    commands_path = os.path.join(PROJECT_DIR_PATH, 'app', 'common', 'management', 'commands', '')
    remove_file(os.path.join(commands_path, 'auto_createsuperuser.py'))


def remove_login_by_social_accounts():
    # TODO
    pass


def generate_random_string(length,
                           using_digits=False,
                           using_ascii_letters=False,
                           using_punctuation=False):
    """
    Example:
        opting out for 50 symbol-long, [a-z][A-Z][0-9] string
        would yield log_2((26+26+50)^50) ~= 334 bit strength.
    """
    if not using_sysrandom:
        return None

    symbols = []
    if using_digits:
        symbols += string.digits
    if using_ascii_letters:
        symbols += string.ascii_letters
    if using_punctuation:
        symbols += string.punctuation \
            .replace('"', '') \
            .replace("'", '') \
            .replace('\\', '')
    return ''.join([random.choice(symbols) for _ in range(length)])


def set_flag(file_path,
             flag,
             value=None,
             *args,
             **kwargs):
    if value is None:
        random_string = generate_random_string(*args, **kwargs)
        if random_string is None:
            import sys
            sys.stdout.write(
                "We couldn't find a secure pseudo-random number generator on your system. "
                "Please, make sure to manually {} later.".format(flag)
            )
            random_string = flag
        value = random_string

    with open(file_path, 'r+') as f:
        file_contents = f.read().replace(flag, value)
        f.seek(0)
        f.write(file_contents)
        f.truncate()

    return value


def set_django_secret_key(file_path):
    django_secret_key = set_flag(
        file_path,
        '!!!SET DJANGO_SECRET_KEY!!!',
        length=50,
        using_digits=True,
        using_ascii_letters=True
    )
    return django_secret_key


def set_postgres_user(file_path,
                      value=None):
    postgres_user = set_flag(
        file_path,
        '!!!SET POSTGRES_USER!!!',
        value=value,
        length=8,
        using_ascii_letters=True
    )
    return postgres_user


def set_postgres_password(file_path):
    postgres_password = set_flag(
        file_path,
        '!!!SET POSTGRES_PASSWORD!!!',
        length=42,
        using_digits=True,
        using_ascii_letters=True
    )
    return postgres_password


def initialize_dotenv(postgres_user):
    # Create env directory to store env file
    dotenv_dir_path = os.path.join(PROJECT_DIR_PATH, 'env')
    if not os.path.exists(dotenv_dir_path):
        os.makedirs(dotenv_dir_path)

    # Initialize dev env file
    dev_env_example_file_path = os.path.join(PROJECT_DIR_PATH, 'dev.env.example')
    set_django_secret_key(dev_env_example_file_path)

    dev_dotenv_file_path = os.path.join(dotenv_dir_path, 'dev.env')
    shutil.move(dev_env_example_file_path, dev_dotenv_file_path)

    # Initialize prod env file
    prod_env_example_file_path = os.path.join(PROJECT_DIR_PATH, 'prod.env.example')
    set_django_secret_key(prod_env_example_file_path)
    set_postgres_user(prod_env_example_file_path, value=postgres_user)
    set_postgres_password(prod_env_example_file_path)

    prod_dotenv_file_path = os.path.join(dotenv_dir_path, 'prod.env')
    shutil.move(prod_env_example_file_path, prod_dotenv_file_path)


def main():
    postgres_user = generate_random_string(length=16, using_ascii_letters=True)
    initialize_dotenv(postgres_user)

    if '{{ cookiecutter.auto_create_super_user }}'.lower() == 'n':
        remove_auto_createsuperuser_file()

    if '{{ cookiecutter.login_by_social_accounts }}'.lower() == 'n':
        remove_login_by_social_accounts()


if __name__ == '__main__':
    main()
