'''
任务：统计每一个同学的作业，1、统计是否运行成功，如果成功，输出成功结果，如果失败，输出失败结果；
                            2、统计代码行数、字符数，备注行数，字符数；
'''
import os
import codecs 
import chardet
import shutil
import time
###获取homework/目录下的所有目录的名称列表 
def get_all_student_dir(path_dir): 
    return os.listdir(path_dir)#['吴晓坤', '林杰颖', '梁志豪', '陈永乐']

###将不同编码的文件转换为utf8文件
def file_convert_to_urt8(filename): 
    try:     
        f=codecs.open(filename,'rb')
        content=f.read() 
        f.close()
        if content is not None:
            source_encoding=chardet.detect(content)['encoding'] #获取原来文件内容的编码格式       
            content=content.decode(source_encoding).encode("utf-8")
            f=codecs.open(filename,'w',"utf-8")
            f.write(str(content, encoding="utf-8"))
            f.close()
            print("convert[debug.py]....from "+source_encoding+" to utf-8")
    except Exception as err: 
        print(err) 
        
###动态运行代码
def run_py(filename):    
    path_str='python %s'%filename   #python homework\陈永乐\debug.py 
    p=os.system(path_str)
    return p    #如果p的值是0，程序执行成功，否则，则是执行错误，有很多种错误分类。

##返回程序代码文件的字符串内容
def return_file_content(filename):
    f=codecs.open(filename,'r',"utf-8")
    content=f.read()   
    return content

##计算备注
def cul_beizhu(lines):
    beizhu=0#备注的字符个数
    beizhu_line=0#备注占据一行的情况
    beizhu_line_total=0#备注的行数
    konghang=0#字符为空的行数
    for line in lines:
        line=line.strip()
        if len(line)==0:
            konghang+=1
        if len(line)!=0 and line[0]=="#":
            beizhu_line+=1
        if "#" in line:
            beizhu_line_total+=1
            num=line.index('#') 
            beizhu=beizhu+len(line[num:])
    return (beizhu,beizhu_line,beizhu_line_total,konghang)

def print_result(name_list,stdent_score):
    with open("result_T12.txt","w") as f:
        for name in name_list:
            print("%s代码检查结果："%name)
            f.write("%s代码检查结果：\n"%name)
            print("代码行数：%d,代码字符数：%d,注释行数：%d"%(stdent_score[name]['code_line'],\
                  stdent_score[name]['code_len'],stdent_score[name]['beizhu_line']))
            f.write("代码行数：%d,代码字符数：%d,注释行数：%d\n"%(stdent_score[name]['code_line'],\
                  stdent_score[name]['code_len'],stdent_score[name]['beizhu_line']))
            if os.path.exists("log\\"+name+"_log.txt"):
                code=return_file_content("log\\"+name+"_log.txt")
                lineList=code.split('\n') 
                print("运行成功，输出行数：%d"%len(lineList))
                f.write("运行成功，输出行数：%d\n"%len(lineList))
            else:
                print("运行失败")
                f.write("运行失败\n")
        f.close()
            
###主程序
def get_homework_info(path_dir,homework):#homework='debug.py'
    name_list=get_all_student_dir(path_dir)
    stdent_score={}
    for name in name_list:
        stdent_score[name]={}
        filename=os.path.join(path_dir,name,homework)         
        filename=filename.replace('/','\\')
        print(filename)         
        file_convert_to_urt8(filename)#把所有同学的debug.py文件的编码格式转换成utf-8
        try:            
            if os.path.exists("log")==False:
                os.mkdir("log")
            p=run_py(filename)#执行同学的代码，如果报错，输出到log/XXX_err.txt,如果成功，输出到log/XXX_log.txt
            time.sleep(3)
            if p==0:#执行成功                
                if os.path.exists("csdn_crawl.txt"):
                    shutil.move("csdn_crawl.txt", "log\\"+name+"_log.txt")
                time.sleep(1)
            else:         
                with open("log\\"+name+"_err.txt","w") as f:
                    f.write(str(p))
                time.sleep(1)
        except Exception as e:
            with open("log\\"+name+"_err.txt","w") as f:
                f.write(str(e))
        code=return_file_content(filename)
        lines=code.split('\n')        
        beizhu,beizhu_line,beizhu_line_total,konghang=cul_beizhu(lines)                         
        stdent_score[name]['code_len']=len(code.replace(' ','').replace('\n','').replace('\r',''))-beizhu#统计代码长度和字符数
        stdent_score[name]['beizhu']=beizhu#统计备注的长度          
        stdent_score[name]['beizhu_line']=beizhu_line_total#备注的行数
        stdent_score[name]['code_line']=len(lines)-beizhu_line-konghang#统计代码的行数 
    print_result(name_list,stdent_score)##输出结果    
    return stdent_score

if __name__=="__main__":
    path='homework/'
    homework='debug.py'
    score_dict=get_homework_info(path,homework)