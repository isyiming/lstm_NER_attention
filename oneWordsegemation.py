#-*-coding:utf-8-*-
import re
import word2vec
import jieba
import numpy as np

def jud(message):
    if "person" in message:
        message = re.sub(r"[\s\n]", "", message)
        marks = ["person","B-PER","I-PER","E-PER"]
        result=deal(message,marks)
    elif "location" in message:
        message = re.sub(r"[\s\n]", "", message)
        marks = ["location","B-LOC","I-LOC","E-LOC"]
        result=deal(message,marks)
    elif "organization" in message:
        message = re.sub(r"[\s\n]", "", message)
        marks = ["organization","B-ORG","I-ORG","E-ORG"]
        result=deal(message,marks)
    elif "o" in message:
        message = re.sub(r"[\s\n]", "", message)
        marks = ["o","o","o","o"]
        result = deal(message,marks)
    else:
        result = [message]
    return result

def deal(message,marks):
    message = message.replace(marks[0],"")
    lists = []
    if len(message)>2:
        lists.append(message[0]+" "+marks[1])
        for i in message[1:-1]:
            lists.append(i+" "+marks[2])
        lists.append(message[-1]+" "+marks[-1])
    elif len(message) == 2:
        lists.append(message[0]+" "+marks[1])
        lists.append(message[1]+" "+marks[-1])
    else:
        lists.append(message[0]+" "+marks[1])
    return lists

def delkonghang(infile1, outfile1):
    infopen = open(infile1, 'r',encoding="utf-8")
    outfopen = open(outfile1, 'w',encoding="utf-8")
    db = infopen.read()
    # outfopen.write(db.rstrip("\n").replace('  ', '\n'))
    outfopen.write(db.replace("\n\n","\n"))
    infopen.close()
    outfopen.close()

def main():
    model = word2vec.load('./199801-onebyone.bin')

    f = open("199801sentenceSplit2.txt","r",encoding="utf-8")
    content = f.readlines()
    w = open("199801-resultOneWordtest.txt","w",encoding="utf-8")
    v = open("199801-resultOneWordtrain.txt","w",encoding="utf-8")

    for num,i in enumerate(content):
        result=jud(i)
        i_f=i.split(' ')
        index=np.where(model.vocab==i_f[0])

        for i in result:
            strvec=''
            vec=(model.vectors[index]).flatten()
            for vecind in vec:
                strvec=strvec+str(vecind)+' '
	    	if num<10000:
	            w.write(i+' '+strvec+"\n")
	        else:
	        	v.write(i+' '+strvec+"\n")
        # if int(num)>100:
        #     break 
    f.close()
    w.close()
    v.close()

    # for i in content:
    #     result=jud(i)
    #     for i in result:
    #         w.write(i+"\n")

    # f.close()
    # w.close()
    delkonghang("199801-resultOneWord.txt","199801-resultOneWordnonekonghang.txt")

if __name__ == '__main__':
	#由文件199801sentenceSplit2，和词向量，得到 ： 词 label 向量
    main()
 
 
 
 
 
 