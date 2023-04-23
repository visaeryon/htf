# Highlights_to_Flashcards
- this is for a niche use case, ofcourse you are free to alter it to suit yours.
- this flashcard is intended to be used with Obsidian SpacedRepetition plugin.
- if you don't want to be bothered with dependencies and requirements, use the releases to get a copy.

## What can it do
- it will take a pdf that is annotated with green and yellow highlighter as input and will output a "%d-%m-%Y.md" file
- green_highlights => questions
- yellow_highlights => answers

## Flashcard Format
```
### GreenHighlight-1
?
- YellowHighlight-1
- YellowHighlight-2

---

### GreenHighlight-2 GreenHighlight-3
?
- YellowHighlight-3
- YellowHighlight-4
```

## Limitations
- The order of resulting flashcard is same as the order in which the highlights are done originally, not in the order of their appearance in a pdf.
- YellowHighlights that follows GreenHighlight-1 will be considered as the answers for the GreenHighlights-1 until GreenHighlight-2 was found.
- Successive GreenHighlights will be considered as the same question, ie., there must be atleast a YellowHighlight between two GreenHighlights for them to be considered different questions.
- line breaks among the same YellowHighlight will be considered two different highlights.

## How to use
- run the htf.exe along with the pdf file you want to extract the highlights from example
```
htf.exe test.pdf
```
or
```
htf.py test.pdf
```
assuming the pdf name is test.pdf and it is in the same directory as the .exe is in
