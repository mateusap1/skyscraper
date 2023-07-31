from bs4 import BeautifulSoup, NavigableString

def extract_content(html_content):
    # Parse the HTML.
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the audio tag
    audio_tag = soup.find('audio')

    # Find the parent of the audio tag
    parent_tag = audio_tag.find_parent()

    # Initialize variables
    between_tags = False
    result_text = []

    # Iterate over all descendants of the parent tag
    for descendant in parent_tag.descendants:
        if descendant == audio_tag:
            between_tags = True
            continue

        if descendant.parent.name == "audio":
            continue

        if between_tags:
            if isinstance(descendant, NavigableString):
                stripped = descendant.strip()
                if stripped:  # check if the string is not empty or whitespace
                    result_text.append(stripped)
            elif descendant.name == 'b' or descendant.find('b') is not None:
                break

    # Print each text string on a new line
    for text in result_text:
        print(text)

# Use the function on your HTML content.
html_content = """
<html>
<body>
    <b>This should not matter</b>
    <span><b>This shouldn't either</b></span>
    <audio src="audio.mp3">This should not be included</audio>
    <div>
        <span>Text that should be included in the output</span>
    </div>
    <p>This is some text between the audio and bold tags</p>
    <i>More text</i>
    <div>
        <span><b>Bold text</b></span>
    </div>
    <p>Some more text after the bold tag</p>
    <b>Other bold text which should not matter either</b>
    <span><b>This shouldn't either</b></span>
</body>
</html>
"""
extract_content(html_content)
