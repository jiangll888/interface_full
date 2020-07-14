import execjs,os

def get_des_psswd(timestamp, key, secrect):
    jsstr = get_js()
    ctx = execjs.compile(jsstr)  # 加载JS文件
    return (ctx.call('fun', timestamp, key, secrect))  # 调用js方法  第一个参数是JS的方法名，后面的data和key是js方法的参数


def get_js():
    md5_js_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"md5.js")
    with open(md5_js_file, 'r', encoding='utf-8') as f: # 打开JS文件
        line = f.readline()
        htmlstr = ''
        while line:
            htmlstr = htmlstr + line
            line = f.readline()
    return htmlstr

if __name__ == '__main__':
    print(get_des_psswd('1565948557195','98555CFA0B844FA2AA5186CA00E5408F','4B90AE5CC08A459DA74BA4A363556982'))