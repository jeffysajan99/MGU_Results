import shutil
import subprocess
import urllib
import os
from BeautifulSoup import BeautifulSoup
import re


class S8btech:

    url = 'http://projects.mgu.ac.in/bTech/btechresult/index.php?' \
          'module=public&attrib=result&page=result&exam=37&Submit2=Submit&prn='
    start, end, filename = 0, 0, "result.csv"
    rankData = []


    def __init__(self):
        try:
            os.mkdir("pdf")
        except:
            pass
        try:
            os.mkdir("tmp")
        except:
            pass

    def get(self, start=0, end=0, filename="result.csv"):
        self.start = start
        self.end = end
        self.filename = filename

        for prn in range(self.start, self.end+1):
            url = self.url + str(prn)
            data = urllib.urlopen(url).read()
            open("pdf/" + str(prn) + ".pdf", "wb").write(data)
            self.pdfToHTML(prn)
        self.publishRankList()


    def pdfToHTML(self, prn):
        subs, mks = [], []
        name, reg, colg, branch, marks, gpa = "", "", "", "", {}, []
        p = subprocess.Popen("convert pdf/" + str(prn) + ".pdf tmp/" + str(prn), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        if os.path.exists("tmp/" + str(prn)):
            bs = BeautifulSoup(open("tmp/" + str(prn) + "/page1.html", "r").read())
            for div in bs.findAll("div"):
                if div and all(x in div["style"] for x in ["top:136px", "left:144px;"]):
                    name = div.text.replace(": ", "")
                elif div and all(x in div["style"] for x in ["left:144px;", "top:108px;"]):
                    colg = div.text.replace(": ", "")
                elif div and all(x in div["style"] for x in ["left:144px;", "top:122px;"]):
                    branch = div.text.replace(": ", "")
                elif div and all(x in div["style"] for x in ["left:144px;", "top:151px;"]):
                    reg = div.text.replace(": ", "")

            f2 = bs.findAll("span", id="f2")
            for span in f2:
                if len(span.text)>1 and str(span.text[0]).isdigit() and span.text[1] == " ":
                    subs.append(span.text[2:])
                if re.match("[\-0-9]+ [\-0-9]+ [\-0-9]+", span.text):
                    mks.append(span.text.split(" "))
                elif re.match("[\-0-9]+ [\-0-9]+", span.text):
                    ind = f2.index(span)
                    mks.append((span.text + " " + f2[ind+1].text).split(" "))

            gpa.append(re.findall("SGPA : ([\-0-9\.]+)", bs.text)[0])
            gpa.append(re.findall("CGPA : ([\-0-9\.]+)", bs.text)[0])

            self.exportResults(name, reg, colg, branch, subs, mks, gpa)
        else:
            l = open(self.filename.split(".")[0] + "_finished.csv", "a")
            l.write("Err, " + str(prn) + "\n")
            l.close()
            print "Err, " + str(prn)


    def exportResults(self, name, reg, colg, branch, subs, marks, gpa):
        if os.path.exists(self.filename):
            f = open(self.filename, "a")
        else:
            f = open(self.filename, "w")
            f.write("RegNum, Name, College, Branch, " +
                    "Subject, Internal, External, Total, " * 8 +
                    "SGPA, CGPA\n")
        for s in range(len(subs)):
            marks[s].insert(0, subs[s])
        mk = ", ".join([", ".join(i) for i in marks])
        data = [reg, name, colg, branch, mk, gpa[0], gpa[1]]
        f.write(", ".join(data) + "\n")
        f.close()
        l = open(self.filename.split(".")[0] + "_finished.csv", "a")
        l.write(reg + ", " + name + "\n")
        l.close()
        print reg, name
        self.rankData.append(data[0:4] + [str(i).strip() for i in data[4].split(",")] + data[5:])
        shutil.rmtree("tmp/" + reg)

    def publishRankList(self):
        displayColumns = [0, 1]
        sortColumns = [7, 11, 15, 27, 31, 35]
        Electives = [19, 23]
        GPA = [37, 36]

        elect_names = [[], []]

        rankFile = open(self.filename.split(".")[0] + "_rankList.csv", "w")

        data = []
        for raw in self.rankData:
            raw = [int(i) if i.isdigit() else i for i in raw]
            data.append([0 if i == '-' else i for i in raw])
            for el in Electives:
                if raw[el-3] not in elect_names[Electives.index(el)]:
                    elect_names[Electives.index(el)].append(raw[el-3])

        # Complete Toppers
        title = "B.Tech Ranklist,,,\n"
        rankFile.write(title)
        data.sort(key=lambda x: x[GPA[0]], reverse=True)
        rankFile.write("\n".join([", ".join([str(data.index(stud)+1)] +
                                            [str(stud[j]) for j in displayColumns+[GPA[0]]]) for stud in data]))
        rankFile.write("\n")
        rankFile.write("\n")
        title = "S8 Ranklist,,,\n"
        rankFile.write(title)
        data.sort(key=lambda x: x[GPA[1]], reverse=True)
        rankFile.write("\n".join([", ".join([str(data.index(stud)+1)] +
                                            [str(stud[j]) for j in displayColumns+[GPA[1]]]) for stud in data]))
        rankFile.write("\n")
        rankFile.write("\n")

        # Subject Toppers
        for i in sortColumns:
            title = raw[i-3] + " Rank,,,\n"
            rankFile.write(title)
            data.sort(key=lambda x: x[i], reverse=True)
            rankFile.write("\n".join([", ".join([str(data.index(stud)+1)] +
                                                [str(stud[j]) for j in displayColumns+[i]]) for stud in data]))
            rankFile.write("\n")
            rankFile.write("\n")

        #  Elective Toppers
        for i in range(2):
            for el in elect_names[i]:
                title = el + " Rank,,,\n"
                rankFile.write(title)
                temp = [s for s in data if s[Electives[i]-3] == el]
                temp.sort(key=lambda x: x[Electives[i]], reverse=True)
                rankFile.write("\n".join([", ".join([str(temp.index(stud)+1)] +
                                                    [str(stud[j])
                                                     for j in displayColumns+[Electives[i]]]) for stud in temp]))
                rankFile.write("\n")
                rankFile.write("\n")


        rankFile.close()



if __name__ == '__main__':
    start = input("Starting Reg Number: ")
    end = input("Ending Reg Number: ")
    filename = raw_input("Enter filename: ")
    S8btech().get(start, end, filename+".csv")



