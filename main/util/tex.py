import subprocess
import shlex
import os
import os.path
import shutil

def compileTex(str, dest):
    tmpDirPath = os.path.realpath("tmp")

    if not os.path.exists(tmpDirPath):
        os.makedirs(tmpDirPath)

    tmpFilePath = os.path.join(tmpDirPath, "tmp.tex")
    tmpPdfFilePath = os.path.join(tmpDirPath, "tmp.pdf")

    tmpFile = open(tmpFilePath, "w")
    tmpFile.write(str)
    tmpFile.close()

    proc = subprocess.Popen(["pdflatex", "-output-directory", "tmp", tmpFilePath])
    proc.communicate()

    shutil.copyfile(tmpPdfFilePath, dest)

def simpleTabular(head, rows, orientation=None):
    out = "\\documentclass{scrartcl}\n\\begin{document}\n"

    numCols = len(head)
    if not orientation:
        orientation = ("l" * numCols)
        
    out += "\\begin{tabular}{" + orientation + "}\n"
    out += (" & ".join(head) + "\\\\\\hline\\hline\n")
    for row in rows:
        row = map(lambda x: str(x), row)
        if(len(row) != numCols):
            raise ValueError("rows must all be of the same size as the head")
        else:
            out += (" & ".join(row) + "\\\\\\hline\n")
    out += "\\end{tabular}\n"
    out += "\\end{document}"

    return out

