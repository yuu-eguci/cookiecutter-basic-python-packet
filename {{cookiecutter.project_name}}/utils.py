"""
Python やるときにいつもあって欲しい自分用モジュールです。
おおよそどのプロジェクトでも使っている utility functions を定義しています。
"""

# Built-in modules.
import logging
import datetime

# Third-party modules.
import pytz
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import mysql.connector

# User modules.
import consts


def get_my_logger(logger_name: str) -> logging.Logger:
    """モジュール用のロガーを作成します。
    logger = get_my_logger(__name__)

    Args:
        logger_name (str): getLogger にわたす名前。 __name__ を想定しています。

    Returns:
        logging.Logger: モジュール用のロガー。
    """

    # ルートロガーを作成します。ロガーはモジュールごとに分けるもの。
    logger = logging.getLogger(logger_name)
    # ルートロガーのログレベルは DEBUG。
    logger.setLevel(logging.DEBUG)
    # コンソールへ出力するハンドラを作成。
    handler = logging.StreamHandler()
    # ハンドラもログレベルを持ちます。
    handler.setLevel(logging.DEBUG)
    # ログフォーマットをハンドラに設定します。
    formatter = logging.Formatter(
        # NOTE: 改行は逆に見づらいので E501 を無視します。
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s')  # noqa: E501
    handler.setFormatter(formatter)
    # ハンドラをロガーへセットします。
    logger.addHandler(handler)
    # 親ロガーへの伝播をオフにします。
    logger.propagate = False
    return logger


def get_now_jst() -> datetime.datetime:
    """datetime.datetime.now を日本時間で取得します。
    NOTE: フォーマットはいつも参照してしまうのでここに note しておきます %Y-%m-%d %H:%M:%S
          あるいは .isoformat() も良い。
    """
    TZ_JAPAN = pytz.timezone('Asia/Tokyo')
    current_jst_time = datetime.datetime.now(tz=TZ_JAPAN)
    return current_jst_time


def send_slack_message(message: str) -> None:
    """Slack にメッセージを送ります。
    """

    slack_client = WebClient(token=consts.SLACK_BOT_TOKEN)
    try:
        # NOTE: unfurl_links は時折鬱陶しいと思っている「リンクの展開機能」です。不要です。 False.
        slack_client.chat_postMessage(
            channel=consts.SLACK_CHANNEL_NAME, text=message, unfurl_links=False)
        # 返却値の確認は行いません。
        # NOTE: Slack api のドキュメントにあるコードなので追加していましたが排除します。
        #       リンクの含まれるメッセージを送信すると、返却値が勝手に変更されるため絶対一致しないからです。
        #       - リンクの前後に <, > がつく
        #       - & -> &amp; エスケープが起こる
        # assert response['message']['text'] == message
    except SlackApiError as e:
        assert e.response['ok'] is False
        # str like 'invalid_auth', 'channel_not_found'
        assert e.response['error']
        logger.error(f'Got an error: {e.response["error"]}')


class DbClient:
    """DB アクセスを行うクラスです。 with 構文で使用可能です。
    with utils.DbClient() as db_client:
        records = db_client.sample_select()
    """

    def __enter__(self):
        mysql_connection_config = {
            'host': consts.MYSQL_HOST,
            'user': consts.MYSQL_USER,
            'password': consts.MYSQL_PASSWORD,
            'database': consts.MYSQL_DATABASE,
        }
        self.connection = mysql.connector.connect(**mysql_connection_config)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    def sample_select(self) -> list:
        """サンプルです。
        Returns:
            list: Select 結果のリスト。
        """

        select_sql = ' '.join([
            'SELECT',
                'id',  # noqa: E131
            'FROM sampletable',
            'WHERE',
                'id = %s',
            'ORDER BY id DESC',
        ])
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(select_sql, (1,))
        records = cursor.fetchall()
        cursor.close()
        return records

    def sample_update(self):
        """サンプルです。
        """

        update_sql = ' '.join([
            'UPDATE sampletable',
            'SET',
                'foo = %s',  # noqa: E131
            'WHERE id = %s',
        ])
        cursor = self.connection.cursor()
        cursor.execute(update_sql, (1, 1))
        cursor.close()
        self.connection.commit()


def get_placeholder(count: int) -> str:
    """count ぶんのプレースホルダ文字列を作ります。
    %s, %s, %s, %s, ...
    Args:
        count (int): 欲しい %s の数。
    Returns:
        str: %s, %s, %s, %s, ...
    """

    return ','.join(('%s' for i in range(count)))


# utils モジュール用のロガーを作成します。
logger = get_my_logger(__name__)

if __name__ == '__main__':
    logger.debug('でばーぐ')
    logger.info('いんーふぉ')
    logger.warning('うぉーにん')
    logger.error('えろあ')
    logger.fatal('ふぇーたる(critical と同じっぽい)')
    logger.critical('くりてぃこぉ')
    logger.debug('get_now_jst -> ' + get_now_jst().isoformat())
    send_slack_message('"utils.py" run for test. Sorry for the notification!')
