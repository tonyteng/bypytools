import os
import click 
import re
import bookmeta

prefix='/mnt/d/temp/book'

def bypy(cmd,preview=True):
    if not cmd.startswith('bypy'):
        cmd='bypy '+cmd
    print(cmd)
    if not preview:
        os.system(cmd)

def bookname(src):
    dest=re.sub(r'【.*】','',src)
    dest=re.sub(r'（.?三秋书屋.?）','',dest)
    return dest

def mvbook(prefix,name,preview):
    with open('%s/%s'%(prefix,name),encoding='utf-8') as f:
        for x in f.readlines()[1:]:
            try:
                print('Line::%s'%x)
                file=x.split(' ')
                #取完整书路径(去除其他信息),书名可能会包含空格
                file=' '.join(file[1:-6])
                #print('file is %s'%file)
                file=file.split('/')
                #print('file[-1] is %s'%file[-1])
                ext=file[-1].split('.')[-1]
                #print('ext is %s'%ext)
                #拼接完整路径(去除 /app/bypy/ 前缀)
                src='/'.join(file[3:])
                #print('src is %s'%src)
                #title=re.sub(r'【.*】','',file[-1])
                title=bookname(file[-1])
                des='dest/%s/%s/%s'%(ext,name,title)
                #print('des is %s'%des)
                if ''!=src.strip():
                    bypy('mv "%s" "%s"'%(src,des),preview)
                    bypy('bypy rm "%s"' % src,preview)
            except Exception as e:
                print(str(e))



def getbook(path):
    titles=[]
    for x in open(path,encoding='utf-8').readlines()[1:]:
        if x.startswith('F /'):
            try:
                title=' '.join(x.split(' ')[1:-6]).split('/')[-1]
                titles.append(title)
            except Exception as e:
                print(str(e))
    return titles

def getbookurl(path):
    urls=[]
    for x in open(path,encoding='utf-8').readlines()[1:]:
        if x.startswith('F /'):
            try:
                title=x.split(' ')[1:-6]
                url='/'.join(' '.join(title).split('/')[3:])
                urls.append(url)
            except Exception as e:
                print(str(e))
    return urls

    #return {'/'.join(' '.join(x.split(' ')[1:-6]).split('/')[3:]) for x in open(path,encoding='utf-8').readlines()}

def getbookdict(path):
    d={}
    for x in open(path,encoding='utf-8').readlines()[1:]:
        if x.startswith('F /'):
            try:
                title=' '.join(x.split(' ')[1:-6]).split('/')[-1]
                url= '/'.join(' '.join(x.split(' ')[1:-6]).split('/')[3:])
                #print('%s=%s'%(title,url))
                title=bookname(title)
                d[title]=url
            except Exception as e:
                print(str(e))
    return d
    #return {' '.join(x.split(' ')[1:-6]).split('/')[-1]: '/'.join(' '.join(x.split(' ')[1:-6]).split('/')[3:]) for x in open(path,encoding='utf-8').readlines()}

def repeatbook():
    os.system('bypy search azw3 dest >dest')
    os.system('bypy search azw3 other >other')
    dest=getbook('dest')
    other=getbook('other')
    p=other&dest
    rmbook(p)

def rmbook(lst):
    d=getbookdict('other')
    for book in lst:
        if book.strip()!='':
            cmd='bypy rm "%s"'%d.get(book)
            print(cmd)
            os.system(cmd)

@click.group()
def cli():
    pass

@click.command()
@click.option('--src',default='yunpan',help='from here read book,default is yunpan.')
@click.option('--preview',default=True,type=bool,help='default is true,just preview')
def addbook(src='yunpan',preview=True):
    '''get book from --src option (default is yunpan), then save book in dest directory'''
    lst=[
    'packt','manning','oreilly','机器学习','数据结构','人工智能','算法','爬虫','安全','node','react','kotlin','angular','javascript','typescript',
    'scrapy',
    'java','python','unix','linux','shell','android','spring','scala',
    'c++','IOS','HTML5','Selenium','WEB','security','ruby','php','docker','kubernetes','GIT','VUE','tcp',
    'vim','regexp','正则表达式','游戏','game','GO语言','树莓派','微信','小程序','SQL','REDIS','mysql','oracle',
    'C#','微服务','wireshark',
    '网络分析','指针','zookeeper','区块链','数学','前端','jquery','CSS','html','测试','unity','hibernate','openstack','图解','代码','敏捷',
    'hadoop','spark','统计学','kafka','bootstrap',
    'mongo','nginx','elast','架构','深度学习','wmware','深入理解','七周',
    'TensorFlow','hive','lua','ext.js','stl','regular','tomcat','numpy','struct','cloud','swift','crack','hack','Electronics',
    'pattern','gis',
    'Learning','Raspberry','mq','window','tomcat','apache','ajax','cpp','make','network','rail',
    'mobi','azw3','pdf','epub','zip'
    ]
    for x in lst:
        bypy('bypy search %s %s > %s/%s'%(x,src,prefix,x),False)
        mvbook(prefix,x,preview)


@click.command()
@click.option('--name',required=True,help="serial's name")
@click.option('--ext', default='', type=click.Choice(['','pdf','mobi','azw3','epub']),help="book's ext,for example:pdf mobi azw3 epub, if no ,means all book will be saved.")
@click.option('--preview',default=True,help='default just to preview',type=bool)
def serial(name,ext,preview):
    '''search /yunpan/ , and save books in serial/NAME'''
    cmd='bypy search %s dest/%s> %s'%(name,ext,name)
    bypy(cmd,False)
    for src in getbookurl(name):
        cmd='bypy cp "%s" "serial/%s/%s/%s"'%(src,name,ext,src.split('/')[-1])
        bypy(cmd,preview)

@click.command()
@click.option('--key',help='定位书名关键字')
@click.option('--dest',help='需要处理的书籍的路径,缺省为dest',default='dest')
@click.option('--replace',help='替换的正则表达式')
@click.option('--target',help='被替换的内容')
def modifyname(key,dest,replace,target):
    '''modify book's name,replace content'''
    cmd='bypy search %s %s >bookname'%(key,dest)
    print("RegExp%s:"%replace)
    print(cmd)
    os.system(cmd)
    for name,url in getbookdict('bookname').items():
        name=re.sub(replace,target,name)
        name='/'.join(url.split('/')[0:-1])+"/"+name
        cmd='bypy mv "%s" "%s"'%(url,name)
        print(cmd)
        os.system(cmd)

@click.command()
@click.option('--key',help='the key to location book')
@click.option('--loc',help='the location to find book ,default is dest')
@click.option('--preview',default=True,help='default just to preview',type=bool)
def delbook(key,loc='dest',preview=True):
    cmd='bypy search %s %s>delbook'%(key,loc)
    print(cmd)
    os.system(cmd)
    for x in getbookurl('delbook'):
        cmd='bypy rm "%s"'%x
        print(cmd)
        if not preview:
            os.system(cmd)

@click.command()
@click.option('--ext',help='file extension',required=True)
@click.option('--src',help='source location,default is yunpan',default='yunpan')
@click.option('--dest',help='dest location,default is dest',default='dest')
@click.option('--preview',default=True,type=bool,help='default is True,just preview mode')
def removerepeat(ext,src,dest,preview=True):
    '''from src folder remove repeat file '''
    bypy('search %s %s>%s.%s'%(ext,src,src,ext),False)
    sb=getbookdict('%s.%s'%(src,ext))
    bypy('search %s %s>%s.%s'%(ext,dest,dest,ext),False)
    db=getbookdict('%s.%s'%(dest,ext))
    for x in sb.keys() & db.keys():
        bypy('rm "%s"'%sb[x],preview)

def getcover(ext,lib,path=None):
    bypy('search %s %s>%s'%(ext,lib,ext),False)
    getcoverbyfile(ext)

@click.command()
@click.option('--file',help='file to be parse,build by bypy search cmd',required=True)
@click.option('--path',help='cover and info save path,default is None')
def getcoverbyfile(file,path=None):
    meta=bookmeta.BookMeta(path)
    try:
        for x in getbook(file):
            meta.get(x)
        if path:
            meta.buildinfo()
    except Exception as e:
        print(str(e))
    finally:
        meta.quit()    

cli.add_command(getcoverbyfile)
cli.add_command(addbook)
cli.add_command(serial)
cli.add_command(modifyname)
cli.add_command(delbook)
cli.add_command(removerepeat)

if __name__=='__main__':
    cli()


