# flameshotによって保存されたスクリーンショットを適切なフォルダへ振り分ける
import os
import sys
import subprocess
import traceback
import shutil

LOG_FILE = os.path.join(os.path.expanduser("~"), '.pic_tidy')
log_remove = True

# 2021-08-07_15-09.png -> ['2021', '08', '07', '15', '09']
def datetime_array(s):
    def mapfn(c):
        if c.isdigit():
            return c
        return ' '
    num_array = list(map(mapfn, s))
    str_array = []
    buf = ""
    for num in num_array:
        if num.isdigit():
            buf += num
        else:
            if len(buf) > 0:
                str_array.append(buf)
            buf = ""
    return str_array

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
    for file in filter(lambda f: f.endswith('.png'), files):
        dt = datetime_array(file)
        if len(dt) < 5:
            continue
        dirname = dt[0] + '_' + dt[1] + '_' + dt[2]
        dirpath = os.path.join(parent, dirname)
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        oldpath = os.path.join(parent, file)
        newpath = os.path.join(dirpath, file)
        log(newpath)
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