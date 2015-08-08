import urllib
import os
from BeautifulSoup import BeautifulSoup
import re


class S8btech:

    url = 'http://projects.mgu.ac.in/bTech/btechresult/index.php?' \
          'module=public&attrib=result&page=result&exam=37&Submit2=Submit&prn='
    start, end = 0, 0
    # subjects = {
    #     "COMPUTER SCIENCE AND ENGINEERING": [
    #         "High Performance Computing",
    #         "Artificial Intelligence",
    #         "Security in Computing",
    #         "Mobile Computing",
    #         "Security in Computing",
    #         "Computer Graphics Lab",
    #         "Project",
    #         "Viva Voce"
    #     ]
    # }

    def __init__(self):
        pass

    def get(self, start=0, end=0):
        self.start = start
        self.end = end

        for prn in range(self.start, self.end+1):
            url = self.url + str(prn)
            data = urllib.urlopen(url).read()
            open("pdf/" + str(prn) + ".pdf", "wb").write(data)
            self.pdfToHTML(prn)

    def pdfToHTML(self, prn):
        subs, mks = [], []
        name, reg, colg, branch, marks, gpa = "", "", "", "", {}, []
        os.system("pdftohtml pdf/" + str(prn) + ".pdf html/" + str(prn))
        bs = BeautifulSoup(open("html/" + str(prn) + "/page1.html", "r").read())
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
            elif re.match("[\-0-9]+ -", span.text):
                ind = f2.index(span)
                mks.append((span.text + " " + f2[ind+1].text).split(" "))

        for sub in subs:
            marks[sub] = mks[subs.index(sub)]

        gpa.append(re.findall("SGPA : ([0-9\.]+)", bs.text)[0])
        gpa.append(re.findall("CGPA : ([0-9\.]+)", bs.text)[0])

        self.exportResults(name, reg, colg, branch, mks, gpa)


    def exportResults(self, name, reg, colg, branch, marks, gpa):
        if os.path.exists("results.csv"):
            f = open("results.csv", "a")
        else:
            f = open("results.csv", "w")
            f.write("RegNum, Name, College, Branch, "
                    "Marks 1 Int, Marks 1 Ext, Marks 1 Tot, "
                    "Marks 2 Int, Marks 2 Ext, Marks 2 Tot, "
                    "Marks 3 Int, Marks 3 Ext, Marks 3 Tot, "
                    "Marks 4 Int, Marks 4 Ext, Marks 4 Tot, "
                    "Elective 1 Int, Elective 1 Ext, Elective 1 Tot, "
                    "Elective 2 Int, Elective 2 Ext, Elective 2 Tot, "
                    "Project Int, Project Ext, Project Tot, "
                    "Viva Voce Int, Viva Voce Ext, Viva Voce Tot, "
                    "SGPA, CGPA\n")
        mk = ", ".join([", ".join(i) for i in marks])
        data = [reg, name, colg, branch, mk, gpa[0], gpa[1]]
        f.write(", ".join(data) + "\n")
        f.close()
        print reg, name


S8btech().get(start=11012367, end=11012367)



