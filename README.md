# dayone2markdown
Converting DayOne journals (from JSON file) into Markdown files.
Based on original version from @ploum.
Compatible with Python3.
The script is intended for conversion of journals into a format compatible with Logseq (md syntax).

## Usage

1. Export you DayOne journal as JSON and unzip the folder.
2. Put the script in the unzipped folder.
3. Run the script `python do2md.py Journal.json`

## Results :

1. Each entry is now converted to an MD file. Name of the file is the date-time of the entry compatible with Logseq's yyyy-mm-dd.md expected format.
   IF there are **multiple entries** at the same day, they are appended into a single file.
2. Pictures are inserted with a relative path compatible with Logseq ( assets/dayone/)
3. Tags are inserted in the text as " #tag" (if they were not previously)
4. Location of an entry is written at the end of the file with both address and coordinates. The Location block is initally collapsed.
5. The script attemps to standardize headers into somewhat uniform format: if the entry beggins with a header, it is preserved. If not, it attempts to find a linebreak in first 30 characters in the entry, and use the first paragraph as header. If not suitable, a "DayOne Entry" header is used. A hashtag (#diary) is appended at the beginning of every header (once per file) to link all the journal files with DayOne diary entries together.
6. The full time of the entry is saved as Logseq page property (publication-date::).

## Limitations

1. I attempted to fix issues occuring with formatting (multiple newlines etc), but formatting issues may still occur. I'll try to fix those over time.
2. Metadata other than tags, time and location are lost.

Work in progress.
