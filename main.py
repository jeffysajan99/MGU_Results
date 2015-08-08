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

            self.exportResults(name, reg, colg, branch, mks, gpa)
        else:
            l = open(self.filename.split(".")[0] + "_finished.csv", "a")
            l.write("Err, " + str(prn) + "\n")
            l.close()
            print "Err, " + str(prn)


    def exportResults(self, name, reg, colg, branch, marks, gpa):
        if os.path.exists(self.filename):
            f = open(self.filename, "a")
        else:
            f = open(self.filename, "w")
            f.write("RegNum, Name, College, Branch, "
                    "Marks 1 Int, Marks 1 Ext, Marks 1 Tot, "
                    "Marks 2 Int, Marks 2 Ext, Marks 2 Tot, "
                    "Marks 3 Int, Marks 3 Ext, Marks 3 Tot, "
                    "Elective 1 Int, Elective 1 Ext, Elective 1 Tot, "
                    "Elective 2 Int, Elective 2 Ext, Elective 2 Tot, "
                    "Lab Int, Lab Ext, Lab Tot, "
                    "Project Int, Project Ext, Project Tot, "
                    "Viva Voce Int, Viva Voce Ext, Viva Voce Tot, "
                    "SGPA, CGPA\n")
        mk = ", ".join([", ".join(i) for i in marks])
        data = [reg, name, colg, branch, mk, gpa[0], gpa[1]]
        f.write(", ".join(data) + "\n")
        f.close()
        l = open(self.filename.split(".")[0] + "_finished.csv", "a")
        l.write(reg + ", " + name + "\n")
        l.close()
        print reg, name
        shutil.rmtree("tmp/" + reg)

if __name__ == '__main__':
    start = input("Starting Reg Number: ")
    end = input("Ending Reg Number: ")
    filename = raw_input("Enter filename: ")
    S8btech().get(start, end, filename+".csv")



