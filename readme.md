# ファイル・ディレクトリバックアップ

requirement:
- schedule

args:
source_path: バックアップしたいファイル・ディレクトリ
backup_path: バックアップ先のディレクトリ
--zip : zipにするかどうかのフラッグ
--number: バックアップファイルの個数
--days: バックアップを行う日数の間隔

使い方例
```
$ python shedule_and_backup.py backup_source/source backup/dir_backup --number 5
```
