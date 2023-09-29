import sys, fitz
from typing import List, Dict
from datetime import datetime
import re

filename = str(sys.argv[1])
doc = fitz.open(filename)

start_page = 3
end_page = len(doc) - 4

plain_text = ""

for page_number in range(start_page, end_page + 1):
    page = doc[page_number]
    plain_text += page.get_text("text")

nine = []
highlights = []
colors = []
previous_color = None
phrase1_list = []
phrase2_list = ["INTERNATIONAL AFFAIRS","NATIONAL AFFAIRS", "IMPORTANT DAYS", "BOOKS & AUTHORS", "STATE NEWS", "OBITUARY", "SPORTS", "SCIENCE & TECHNOLOGY", "ACQUISITIONS & MERGERS", "AWARDS & RECOGNITIONS", "ECONOMY & BUSINESS", "BANKING & FINANCE"]
phrase2_aliases = {
    "INTERNATIONAL AFFAIRS": "sec/international",
    "NATIONAL AFFAIRS": "sec/national",
    "IMPORTANT DAYS": "sec/days",
    "AWARDS & RECOGNITIONS": "sec/awards",
    "STATE NEWS": "sec/state",
    "OBITUARY": "sec/obituary",
    "SPORTS": "sec/sports",
    "SCIENCE & TECHNOLOGY": "sec/sci_tech",
    "BOOKS & AUTHORS": "sec/books",
    "ACQUISITIONS & MERGERS": "sec/acquisitions",
    "ECONOMY & BUSINESS": "sec/economy",
    "BANKING & FINANCE": "sec/banking"
}

def extract_date_from_text(text):
    # Define a regular expression pattern to match the date format "_Month_dd_yyyy_"
    date_pattern = r'_([A-Za-z]+)_(\d{1,2})(?:-\d{1,2})?_(\d{4})_'
    # date_pattern = r'_([A-Za-z]+)_(\d{1,2})(?:-(\d{1,2}))?_(\d{4})_'
    # Search for the date pattern in the input text
    match = re.search(date_pattern, text)
    
    # Check if a match was found
    if match:
        # Extract month, day, and year from the match
        month = match.group(1)
        day = match.group(2)
        year = match.group(3)
        
        # Use the datetime library to parse the month name and format the date
        try:
            date_obj = datetime.strptime(f"{year}-{month}-{day}", "%Y-%B-%d")
            return date_obj
        except ValueError:
            return None
    else:
        # Return None if no date was found
        return None

date_obj = extract_date_from_text(filename)
dte = date_obj.strftime("%d-%m-%Y")
# day = date_obj.day
now = datetime.now().strftime("%I:%M %p").lower()
mth = date_obj.strftime("%b")
wkn = date_obj.strftime("%U")

def concatenate_same_color_text(data):
    result = []
    current_color = None
    current_text = ""
    current_tag = None  # Initialize current_tag variable
    
    for item in data:
        if item["color"] == current_color:
            current_text += " " + item["text"]
        else:
            if current_color is not None:
                # Check if there's a current tag to add
                if current_tag:
                    result.append({"text": current_text.strip(), "color": current_color, "tag": current_tag})
                else:
                    result.append({"text": current_text.strip(), "color": current_color})
            current_color = item["color"]
            current_text = item["text"]
            current_tag = item.get("tag")  # Update current_tag
    
    if current_color is not None:
        if current_tag:
            result.append({"text": current_text.strip(), "color": current_color, "tag": current_tag})
        else:
            result.append({"text": current_text.strip(), "color": current_color})
    
    return result

def format_flashcards(data):
    current_heading = ""
    output = ""
    previous_tag = "sec/national"
    
    for item in data:
        # print(item)
        if item["color"] == (1.0, 1.0, 0.0):  # Yellow color indicates a new heading
            if current_heading:  # If there was a previous heading, add it with its content
                output += current_heading + "\n"
            # print(item["tag"])  
            tag = item.get("tag", previous_tag)
            current_heading = "\n---\n\n#" + tag + "\n# " + item["text"] + "\n?" # Start a new heading
            previous_tag = tag
            # print(current_heading)
        else:  # Green and red colors are treated as content under the current heading
            if current_heading:
                current_heading += "\n- " + item["text"]

    # Add the last heading with its content
    if current_heading:
        output += current_heading + "\n\n---"
    
    output = "---\nDate: "+ dte + "\nTime: " + now + "\nTags: " + "ca/" + mth + "/week_"+ wkn + "\n---\n""\n# " + dte + output
    
    return output

for page in doc:
    annot = page.first_annot
    while annot:
        if annot.type[0] == 8 or 9:
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

# Iterate through the list to collect "phrase1" text values
for item in nine:
    current_color = item.get('color')

    # Check if the current color is (1.0, 1.0, 0.0) and is not consecutive
    if current_color == (1.0, 1.0, 0.0) and current_color != previous_color:
        phrase1_list.append(item.get('text'))

    previous_color = current_color
# print(phrase1_list)
# Initialize a set to keep track of found phrases
found_phrases_set = set()

# Initialize a list to store found phrases and their positions
found_phrases = []

# Iterate through phrase1_list and phrase2_list and search for occurrences
for phrase in phrase1_list + phrase2_list:
    start = 0
    while start < len(plain_text):
        pos = plain_text.find(phrase, start)
        if pos != -1 and phrase not in found_phrases_set:
            found_phrases_set.add(phrase)
            found_phrases.append((phrase, pos))
            start = pos + len(phrase)
        else:
            # print(phrase)
            #  Check for "text" matching and "color" matching in "nine"
            for item in nine:
                if item["text"] == phrase and item["color"] == (1.0, 1.0, 0.0):
                    # found_phrases_set.add(phrase)
                    # print(found_phrases_set)
                    # print(found_phrases)
                    # print(phrase)
                    # print(found_phrases.append((phrase, pos)))
                #     found_phrases.append((phrase, pos))
                #     start = pos + len(phrase)
                    break
                # else:
        break	

# Sort the found phrases by their positions
sorted_phrases = sorted(found_phrases, key=lambda x: x[1])

# Extract only the phrases from the sorted list
sorted_phrase_list = [phrase for phrase, _ in sorted_phrases]

# Initialize a list to store the objects
tagged_objects = []

# Initialize variables to keep track of the current tag and text
current_tag = None
current_text = None

# Iterate through the sorted phrases
for phrase in sorted_phrase_list:
    if phrase in phrase2_list:
        current_tag = phrase
    elif current_tag is not None:
        current_text = phrase
        tagged_objects.append({"tag": current_tag, "text": current_text})

for tagged_item in tagged_objects:
    current_tag = tagged_item.get('tag')

    # Check if the current tag is in phrase2_list
    if current_tag in phrase2_list:
        tagged_item['tag'] = phrase2_aliases.get(current_tag, current_tag)

for item in nine:
    current_text = item.get('text')

    # Find the matching item in "tagged_objects" based on text
    matching_tagged_item = next((tagged_item for tagged_item in tagged_objects if tagged_item['text'] == current_text), None)

    # If a matching item is found, add its "tag" field to the current item in "nine"
    if matching_tagged_item:
        item['tag'] = matching_tagged_item['tag']

concatenated_nine = concatenate_same_color_text(nine)
# for i in concatenated_nine:
    # print(i["color"], i["tag"])
out = format_flashcards(concatenated_nine)

with open(f'{dte}.md', 'w', encoding="utf-8") as f:
    f.write(out)
