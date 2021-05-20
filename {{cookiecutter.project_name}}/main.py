"""{{cookiecutter.project_name}} main module
"""

# Built-in modules.

# User modules.
import utils
import functions


def run():
    """メインの実行関数です。
    NOTE: 他のモジュール……特に定期実行モジュール……から呼ばれることも想定して
          関数化しています。
    """

    # ロガーを取得します。
    logger = utils.get_my_logger(__name__)
    now_jst = utils.get_now_jst()
    logger.info(f'Main module started at {now_jst.isoformat()}')


if __name__ == '__main__':
    run()
