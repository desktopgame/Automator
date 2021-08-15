# 「フォルダアクション」用のテンプレート
# 入力の引き渡し方法は「引数として」を選択すること
import os
import sys
import subprocess
import traceback

#LOG_FILE = os.path.join(os.path.expanduser("~"), '.folder_action')
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