"""
Python やるときにいつもあって欲しい自分用モジュールです。
リテラルや環境変数によって、定数を定義します。
NOTE: 長いこと、 python-dotenv によって環境変数を読み込んでいました。
      しかし pipenv 内では .env から os.environ で直接取得できると知り卒業しました。
"""

# Built-in modules.
import os


def get_env(keyname: str, allow_empty: bool = False) -> str:
    """環境変数を取得します。
    NOTE: 設定されていないときは例外が欲しいため、 os.environ をラップしています。
          環境によっては(というか GitHub Actions)、環境変数が設定されていなくても
          空文字列が入ってしまいます。

    Args:
        keyname (str): 環境変数名。
        allow_empty (bool, optional): 空文字列でもいいよ。 Defaults to False.

    Raises:
        KeyError: そんな環境変数は無い。

    Returns:
        str: 環境変数の値。
    """
    # そんな環境変数は存在しない場合、ここで KeyError です。
    # NOTE: os.getenv を使った場合、例外でなく None が返ります。
    _ = os.environ[keyname]
    if not _:
        raise KeyError(f'{keyname} is empty.')
    return _


FOO = get_env('FOO')

if __name__ == '__main__':
    print(repr(FOO))
