import os

prefix='/mnt/d/temp/book'
def mvbook(prefix,name):
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
                des='dest/%s/%s/%s'%(ext,name,file[-1])
                #print('des is %s'%des)
                if ''!=src.strip():
                    print('bypy mv "%s" "%s"\n'%(src,des))
                    os.system('bypy mv "%s" "%s"'%(src,des))
                    os.system('bypy rm "%s"' % src)
            except Exception as e:
                print(str(e))

def sbook():
    lst=[
    #'packt','manning','oreilly','机器学习','数据结构','人工智能','算法','爬虫','安全','node','react','kotlin','angular','javascript','typescript',
    #'scrapy',
    #'java','python','unix','linux','shell','android','spring','scala',
    #'c++','IOS','HTML5','Selenium','WEB','security','ruby','php','docker','kubernetes','GIT','VUE','tcp',
    #'vim','regexp','正则表达式','游戏','game','GO语言','树莓派','微信','小程序','SQL','REDIS','mysql','oracle',
    #'C#','微服务','wireshark',
    #'网络分析','指针','zookeeper','区块链','数学','前端','jquery','CSS','html','测试','unity','hibernate','openstack','图解','代码','敏捷',
    #'hadoop','spark','统计学','kafka','bootstrap',
    #'mongo','nginx','elast','架构','深度学习','wmware','深入理解','七周',
    #'TensorFlow','hive','lua','ext.js','stl','regular','tomcat','numpy','struct','cloud','swift','crack','hack','Electronics',
    #'pattern','gis',
    #'Learning','Raspberry','mq','window','tomcat','apache','ajax','cpp','make','network','rail',
    'mobi','azw3','pdf','epub','zip'
    ]
    for x in lst:
        print('bypy search %s yunpan'%x)
        #os.system('bypy search %s computer | wc -l'%x)
        os.system('bypy search %s yunpan > %s/%s'%(x,prefix,x))
        mvbook(prefix,x)

#删除重复书籍
def getbook(path):
    return {' '.join(x.split(' ')[1:-6]).split('/')[-1] for x in open(path,encoding='utf-8').readlines()}

def getbookurl(path):
    urls=[]
    for x in open(path,encoding='utf-8').readlines():
        try:
            title=x.split(' ')[1:-6]
            url='/'.join(' '.join(title).split('/')[3:])
            urls.append(url)
        except Exception as e:
            print(str(e))
    return urls[1:]

    #return {'/'.join(' '.join(x.split(' ')[1:-6]).split('/')[3:]) for x in open(path,encoding='utf-8').readlines()}

def getbookdict(path):
    return {' '.join(x.split(' ')[1:-6]).split('/')[-1]: '/'.join(' '.join(x.split(' ')[1:-6]).split('/')[3:]) for x in open(path,encoding='utf-8').readlines()}

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


def serial(name,ext=''):
    cmd='bypy search %s dest/%s> %s'%(name,ext,name)
    print(cmd)
    os.system(cmd)
    for src in getbookurl(name):
        cmd='bypy cp "%s" "serial/%s/%s/%s"'%(src,name,ext,src.split('/')[-1])
        print(cmd)
        os.system(cmd)

#repeatbook()       
    
#从 bypy/yunpan目录 move到dest/分类目录中
sbook()


#搜索系列图书并cp至对应的目录
#serial('Head')
#serial('mysql')
#serial('redis')

#serial('react')
#serial('action','pdf')
#serial('action','mobi')
#serial('python')
#serial('javascript')
#serial('android')