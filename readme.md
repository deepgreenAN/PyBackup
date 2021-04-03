# ファイル・ディレクトリバックアップ

## requirement
- schedule
## test
クローンしたディレクトリで
```
python setup.py test
```

## installation
```
pip install git+https://github.com/deepgreenAN/py_backup.git
```
あるいはクローンしたディレクトリで
```
python setup.py install
```

## 使い方
### バックアッププログラムを利用する場合
クローンしたディレクトリで以下のように実行するか

```
$ python schedule_and_backup.py backup_source/source backup/dir_backup --zip --number 5
```
インストールした後以下のコマンドラインを実行する
```
$schedule_and_backup backup_source/source backup/dir_backup --number 3 --days 5
```
ここで引数は順番通りに以下となる．

args:
- source_path: バックアップしたいファイル・ディレクトリ  
- backup_path: バックアップ先のディレクトリ  
- --zip : zipにするかどうかのフラッグ(指定するとzipファイルに変換して保存される)
- --number: バックアップファイルの個数(デフォルトは5)
- --days: バックアップを行う日数の間隔(デフォルトは7)  

このプログラムでは，ローカルシステムの午前0時にバックアップが開始される．
### 他のスケジューリングプログラムで利用する場合

使い方例
```python
from schedule_and_backup import PyBackUp
from pathlib import Path

source_path = Path("backup_source/source")
backup_path = Path("backup/dir_backup")

pybackup = PyBackUp(source_path=source_path,
                    backup_path=backup_path,
                    back_number=5,
                    to_zip=True
                    )

# バックアップを行う
pybackup.back_up()
```