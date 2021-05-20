"""scheduled_worker.py
定期実行されることを想定しているスクリプトです。
"""

# User modules.
import utils
import functions

# このモジュール用のロガーを作成します。
logger = utils.get_my_logger(__name__)


def run():

    # main module を起動するかどうか判断します。
    # TODO: Implement.
    logger.debug('scheduled_worker')


if __name__ == '__main__':
    try:
        run()
    except Exception as ex:
        # NOTE: str(ex) によりメッセージが出力されます。
        utils.send_slack_message(f'Error raised in scheduled_worker: {ex}\n')
