import xml.etree.ElementTree as ET
import re
import string

XmlFile = 'Q3/samplehyp.xml'
LineBased = 'Q3/Line-Based.txt'
tree = ET.parse(XmlFile)
root = tree.getroot()

CleanedLines = []
for seg in root.findall('.//seg'):
    if seg.text:
        text = seg.text
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = re.sub(r'\s+', ' ', text).strip()
        if text:
            CleanedLines.append(text)

with open(LineBased, 'w', encoding='utf-8') as f:
    for line in CleanedLines:
        f.write(line + '\n')

#Shell commands to create BPE vocabulary
#git clone https://github.com/rsennrich/subword-nmt.git
#python subword-nmt/subword_nmt/learn_bpe.py -s 2000 < Line-Based.txt > vocabulary.bpe
