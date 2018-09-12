import re

def getlabel(content):
    labels = []
    for i in content:
        i=i.replace(r"/","")
        i = re.findall(r"[\u4e00-\u9fa5onsntnr，。！、]+",i)
        # number = i.count("o")
        # for num in range(number):
        #     i.remove("o")
        labels.append(i)
    # print(labels)
    return labels

def getsentence(content):
    sentence = []
    for item in content:
        item = re.findall(r"[\u4e00-\u9fa5]+",item)
        # print(item)
        item = "".join(item)
        sentence.append(item)
    # print(sentence)
    return sentence

def writefile(content):
    f = open("result.txt","w",encoding="utf-8")
    for i in content:
        print(i)
        f.write("\n")
        for j in i:
            if j[-2:] == "ns" or j[-2:] == "nr" or j[-2:] == "nt":
                strings = j[:-2]
                label = j[-2:]
                for k in strings:
                    f.write(k+"\t"+label+"\n")
            else:
                strings = j[:-1]
                label = j[-1]
                for k in strings:
                    f.write(k+"\t"+label+"\n")
    f.close()

def main():
    f = open("aa.txt",encoding="utf-8")
    content = f.read()
    content = content.split("\n")
    # result_sentence = getsentence(content)
    result_label = getlabel(content)
    writefile(result_label)

if __name__ == "__main__":
    main()