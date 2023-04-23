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
GreenHighlight-1
?
YellowHighlight-1
YellowHighlight-2
---
GreenHighlight-2 GreenHighlight-5
?
YellowHighlight-3
YellowHighlight-4
```

## Limitations
- YellowHighlights that follows GreenHighlight-1 will be considered as the answers for the GreenHighlights-1 until GreenHighlight-2 was found.
- The order of execution is same as the order in which it is highlighted originally, not in the order of appearance.
- ~~Questions can't be of multiple hihglights, even if it is in the same line, that is one big non-split green highlight is required.~~

## HOW to use
- run the htf.exe along with the pdf file you want to extract the highlights from example
```
htf.exe test.pdf
```
assuming the pdf name is test.pdf and it is in the same directory as the .exe is in
