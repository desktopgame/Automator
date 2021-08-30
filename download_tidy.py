# ダウンロードされたファイルを適切なフォルダへ振り分ける
import os
import sys
import subprocess
import traceback
import shutil

LOG_FILE = os.path.join(os.path.expanduser("~"), '.download_tidy')
log_remove = True

def main(log):
    global log_remove
    # ファイルアクションの場合、argv[1]に対象ファイルが入るので
    # 引数の長さが足りない場合は無視する
    args = sys.argv
    log('-')
    for a in args:
        log(a)
    log('-')
    if len(args) < 2:
        return
    filepath = args[1]
    # 処理ファイルの親ディレクトリを取得する
    parent = os.path.dirname(filepath)
    # TODO: ここに実際の処理を記述する
    files = os.listdir(parent)
    for file in files:
        fn, ext = os.path.splitext(file)
        if len(ext) == 0:
            continue
        if not os.path.isfile(os.path.join(parent, file)) and not ext == '.app':
            continue
        log(file)
        ext = ext.replace('.', '_')
        to_dir = os.path.join(parent, ext)
        if not os.path.exists(to_dir):
            os.mkdir(to_dir)
        oldpath = os.path.join(parent, file)
        newpath = os.path.join(to_dir, file)
        if os.path.exists(newpath):
            to_dir = os.path.join(parent, '_dup')
            if not os.path.exists(to_dir):
                os.mkdir(to_dir)
            newpath = os.path.join(to_dir, file)
        try:
            shutil.move(oldpath, newpath)
            os.remove(oldpath)
        except:
            pass


# 実行状況をログファイルに出力する
with open(LOG_FILE, 'w+') as fp:
    log_list = []
    try:
        log = lambda s: fp.write(s + '\n')
        log('start')
        main(log)
        log('end')
    except:
        log(traceback.format_exc())
        log_remove = False

if log_remove:
    os.remove(LOG_FILE)