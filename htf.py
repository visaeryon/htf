import sys, fitz
from typing import List, Dict
import datetime

filename = str(sys.argv[1])
doc = fitz.open(filename)

nine = []
highlights = []
colors = []

def format_flashcards(data: List[Dict[str, str]]) -> List[str]:
    current_heading = ""
    output = ""
    for item in data:
        if item["color"] == (0.0,1.0,0.0):
            if current_heading == "":
                current_heading = "\n---\n\n" + "# " + item["text"]
            else:
                output += current_heading + " "
                current_heading = item["text"]
        else:
            if current_heading != "":
                output += current_heading + "\n?\n"
                current_heading = ""
            output += "- " + item["text"] + "\n"
    if current_heading != "":
        output += current_heading + "\n?\n"
    return output

for page in doc:
    annot = page.first_annot
    while annot:
        if annot.type[0] == 8:
            all_coordinates = annot.vertices
            all_words = page.get_text("words")
            if len(all_coordinates) == 4:   
                highlight_coord = fitz.Quad(all_coordinates).rect
                sentence = [w[4] for w in all_words if fitz.Rect(w[0:4]).intersects(highlight_coord)]
                highlights.append(" ".join(sentence))
                colors.append(annot.colors['stroke'])
            else:
                all_coordinates = [all_coordinates[x:x+4] for x in range(0, len(all_coordinates), 4)]
                for i in range(0,len(all_coordinates)):
                    coord = fitz.Quad(all_coordinates[i]).rect
                    sentence = [w[4] for w in all_words if fitz.Rect(w[0:4]).intersects(coord)]
                    highlights.append(" ".join(sentence))
                    colors.append(annot.colors['stroke'])
        annot = annot.next
    
for i in range(len(highlights)):
    obj = {'text': highlights[i], 'color': colors[i]}
    nine.append(obj)

out = format_flashcards(nine)

now = datetime.datetime.now()
date_str = now.strftime("%d-%m-%Y")

with open(f'{date_str}.md', 'w') as f:
    f.write(out)