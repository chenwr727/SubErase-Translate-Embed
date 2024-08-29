import datetime


def update_status(message: str) -> None:
    """
    记录并打印操作状态信息，包含时间戳和固定作用域标签。

    Args:
        message (str): 要记录的状态信息。
    """
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{now_str}: {message}")
