from pathlib import Path
import argparse
import schedule
import time
import datetime

from py_backup import PyBackUp

def main():
    print("[{}] schedule program start".format(str(datetime.datetime.now())))
    parser = argparse.ArgumentParser(description='back up by shchedule')

    parser.add_argument("source_path", help="ソースファイル・ディレクトリ")
    parser.add_argument("backup_path", help="バックアップディレクトリ")
    parser.add_argument("--zip", action="store_true", help="zipファイルにするかどうか")
    parser.add_argument("--number", help="バックアップファイルの個数", type=int, default=5)
    parser.add_argument("--days", help="バックアップの間隔日数", type=int, default=7)

    args = parser.parse_args()

    source_path = Path(args.source_path)
    backup_path = Path(args.backup_path)

    pybackup = PyBackUp(source_path=source_path,
                        backup_path=backup_path,
                        back_number=args.number,
                        to_zip=args.zip
                        )
    
    # 一度行う
    pybackup.back_up()

    if args.days != 1:
        schedule.every(args.days).days.at("12:00").do(pybackup.back_up)
    else:
        schedule.every().day.at("12:00").do(pybackup.back_up)

    while True:
        schedule.run_pending()
        time.sleep(1)  # 一秒単位で更新

if __name__ == "__main__":
    main()