import unittest
from pathlib import Path
import zipfile
import shutil
import datetime
import time

from py_backup import PyBackUp, make_zip



class TestMakeZip(unittest.TestCase):
    def test_make_zip_simple(self):
        temp_file_path = Path("test/temp.txt")
        temp_zip_path = Path("test/temp_zip.zip")
        
        written_str = "hello!"
        
        with open(temp_file_path, "w") as f:
            f.write(written_str)
            
        make_zip(temp_file_path, temp_zip_path)
        
        with zipfile.ZipFile(temp_zip_path) as fzip:
            with fzip.open("temp.txt") as finz:
                read_str = finz.read().decode()  # 厳密にはエンコーディングが必要
                        
        self.assertEqual(written_str, read_str)
        
        temp_file_path.unlink()
        temp_zip_path.unlink()
    
    
    def test_make_zip_nest(self):
        temp_file_parent = Path("test/temp")
        if not temp_file_parent.exists():
            temp_file_parent.mkdir()
        temp_file_path = temp_file_parent / Path("temp.txt")
        
        temp_source_path = Path("test/temp")
        
        temp_zip_path = Path("test/temp_zip.zip")
        
        written_str = "hello!"
        
        with open(temp_file_path, "w") as f:
            f.write(written_str)
            
        make_zip(temp_source_path, temp_zip_path)
        
        with zipfile.ZipFile(temp_zip_path) as fzip:
            with fzip.open("temp/temp.txt") as finz:
                read_str = finz.read().decode()  # 厳密にはエンコーディングが必要
                        
        self.assertEqual(written_str, read_str)
        
        temp_file_path.unlink()
        shutil.rmtree(temp_file_parent)



class TestBackup(unittest.TestCase):
    def _get_all_backup_datetime(self, backup_dir_path):
        backup_dirs = backup_dir_path.iterdir()
        datetime_list = []
        for backup_dir in backup_dirs:
            backup_file_first = list(backup_dir.iterdir())[0]
            if backup_file_first.is_file():  # ファイルだった場合
                backup_file_path_any = backup_file_first
                
            else:  # ディレクトリだった場合
                backup_file_first_first = list(backup_file_first.iterdir())[0]
                backup_file_path_any = backup_file_first_first
                
            update_timestamp = backup_file_path_any.stat().st_mtime
            update_datetime = datetime.datetime.fromtimestamp(update_timestamp)
            datetime_list.append(update_datetime)
            
        return datetime_list
    
    def _get_latest_backup_path(self, backup_dir_path):
        backup_dir_list = list(backup_dir_path.iterdir())
        datetime_list = self._get_all_backup_datetime(backup_dir_path)
        lately_datetime_index = datetime_list.index(max(datetime_list))
        return backup_dir_list[lately_datetime_index]
    
    def _read_backup_raw(self, one_backup_dir_path, relative_path):
        backup_file_path = one_backup_dir_path / relative_path
        with open(backup_file_path, "r") as f:
            read_str = f.read()
            
        return read_str
    
    def _read_backup_zip(self, one_backup_dir_path, zipfile_name, relative_from_zip):
        with zipfile.ZipFile(one_backup_dir_path / zipfile_name) as fzip:
            with fzip.open(str(relative_from_zip)) as finz:
                read_str = finz.read().decode()
        return read_str
    
    def setUp(self):
        temp_backup_dir = Path("test/backup")
        self.assertFalse(temp_backup_dir.exists())
        if not temp_backup_dir.exists():
            temp_backup_dir.mkdir()
            
        temp_source_dir = Path("test/source")
        self.assertFalse(temp_source_dir.exists())
        if not temp_source_dir.exists():
            temp_source_dir.mkdir()
    
    def tearDown(self):
        # バックアップファイルを全て削除
        temp_backup_dir = Path("test/backup")
        self.assertTrue(temp_backup_dir.exists())
        shutil.rmtree(temp_backup_dir)
        
        temp_source_dir = Path("test/source")
        self.assertTrue(temp_source_dir.exists())
        shutil.rmtree(temp_source_dir)
    
    def test_backup_simple_raw(self):
        backup_number = 2
        temp_source_path = Path("test/temp.txt")
        temp_backup_dir = Path("test/backup")
            
        if not temp_source_path.exists():
            temp_source_path.touch()
        
        backupper = PyBackUp(temp_source_path, temp_backup_dir, backup_number, to_zip=False)
        backup_relative_path = Path("temp.txt")
        
        # バックアップとチェック
        for i in range(backup_number+1):
            written_str = "hello!"*i
            # ソースファイルの書き換え
            with open(temp_source_path, "w") as f:
                f.write(written_str)
            
            # バックアップ
            backupper.back_up()
            time.sleep(3) # ファイル作成の時間取得の誤差のため
            
            # 最新のバックアップファイルを取得
            latest_backup_dir_path = self._get_latest_backup_path(temp_backup_dir)
            
            read_str = self._read_backup_raw(latest_backup_dir_path, backup_relative_path)
            self.assertEqual(written_str, read_str)
            
        # バックアップディレクトリの数
        self.assertEqual(len(list(temp_backup_dir.iterdir())), backup_number)
        
    def test_backup_simple_zip(self):
        backup_number = 2
        temp_source_path = Path("test/temp.txt")
        temp_backup_dir = Path("test/backup")
            
        if not temp_source_path.exists():
            temp_source_path.touch()
        
        backupper = PyBackUp(temp_source_path, temp_backup_dir, backup_number, to_zip=True)
        
        zip_name = Path("temp.zip")
        relative_from_zip = Path("temp.txt")
        
        # バックアップとチェック
        for i in range(backup_number+1):
            written_str = "hello!"*i
            # ソースファイルの書き換え
            with open(temp_source_path, "w") as f:
                f.write(written_str)
            
            # バックアップ
            backupper.back_up()
            time.sleep(3) # ファイル作成の時間取得の誤差のため
            
            # 最新のバックアップファイルを取得
            latest_backup_dir_path = self._get_latest_backup_path(temp_backup_dir)
            
            read_str = self._read_backup_zip(latest_backup_dir_path, zip_name, relative_from_zip)
            self.assertEqual(written_str, read_str)
            
        # バックアップディレクトリの数
        self.assertEqual(len(list(temp_backup_dir.iterdir())), backup_number)
        
    def test_backup_nest_zip(self):
        backup_number = 2
        temp_source_path = Path("test/source")
        temp_backup_dir = Path("test/backup")
        
        temp_source_file_path = temp_source_path / Path("temp.txt")
        if not temp_source_file_path.exists():
            temp_source_file_path.touch()
        
        backupper = PyBackUp(temp_source_path, temp_backup_dir, backup_number, to_zip=False)
        backup_relative_path = Path("source/temp.txt")
        
        # バックアップとチェック
        for i in range(backup_number+1):
            written_str = "hello!"*i
            # ソースファイルの書き換え
            with open(temp_source_file_path, "w") as f:
                f.write(written_str)
            
            # バックアップ
            backupper.back_up()
            time.sleep(3) # ファイル作成の時間取得の誤差のため
            
            # 最新のバックアップファイルを取得
            latest_backup_dir_path = self._get_latest_backup_path(temp_backup_dir)
            
            read_str = self._read_backup_raw(latest_backup_dir_path, backup_relative_path)
            self.assertEqual(written_str, read_str)
            
        # バックアップディレクトリの数
        self.assertEqual(len(list(temp_backup_dir.iterdir())), backup_number)
        
        def test_backup_nest_raw(self):
            backup_number = 2
            temp_source_path = Path("test/source")
            temp_backup_dir = Path("test/backup")

            temp_source_file_path = temp_source_path / Path("temp.txt")
            if not temp_source_file_path.exists():
                temp_source_file_path.touch()

            backupper = PyBackUp(temp_source_path, temp_backup_dir, backup_number, to_zip=False)

            zip_name = Path("temp.zip")
            relative_from_zip = Path("source/temp.txt")

            # バックアップとチェック
            for i in range(backup_number+1):
                written_str = "hello!"*i
                # ソースファイルの書き換え
                with open(temp_source_file_path, "w") as f:
                    f.write(written_str)

                # バックアップ
                backupper.back_up()
                time.sleep(3) # ファイル作成の時間取得の誤差のため

                # 最新のバックアップファイルを取得
                latest_backup_dir_path = self._get_latest_backup_path(temp_backup_dir)

                read_str = self._read_backup_zip(latest_backup_dir_path, zip_name, relative_from_zip)
                self.assertEqual(written_str, read_str)

            # バックアップディレクトリの数
            self.assertEqual(len(list(temp_backup_dir.iterdir())), backup_number)


if __name__ == "__main__":
    unittest.main()