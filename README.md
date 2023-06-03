# Highlights_to_Flashcards
- this is for a niche use case, ofcourse you are free to alter it to suit yours.
- this flashcard is intended to be used with Obsidian SpacedRepetition plugin.
- if you don't want to be bothered with dependencies and requirements, use the releases to get a copy.

## What can it do
- it will take a pdf that is annotated with green underline and yellow highlight as input and will output a "%d-%m-%Y.md" file
- YellowHighlights => questions
- GreenUnderline => answers

## Flashcard Format
```
### YellowHighlight-1
?
- GreenUnderline-1
- GreenUnderline-2

---

### YellowHighlight-2 YellowHighlight-3
?
- GreenUnderline-3
- GreenUnderline-4
```

## Limitations
- The order of resulting flashcard is same as the order in which the highlights are done originally, not in the order of their appearance in a pdf.
- GreenUnderline that follows YellowHighlight-1 will be considered as the answers for the YellowHighlight-1 until YellowHighlight-2 was found.
- Successive YellowHighlights will be considered as the same question, ie., there must be atleast a GreenUnderline between two YellowHighlights for them to be considered different questions.
- line breaks among the same GreenUnderline will be considered two different Underlines.

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
