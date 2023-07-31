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
    temp_text = ""

    # Iterate over all descendants of the parent tag
    for descendant in parent_tag.descendants:
        if descendant == audio_tag:
            between_tags = True
            continue

        if between_tags:
            if isinstance(descendant, NavigableString):
                temp_text += descendant.strip()
            elif descendant.name == 'b' or descendant.find('b') is not None:
                if temp_text:
                    result_text.append(temp_text)
                    temp_text = ""
                break
            elif descendant.name in ['p', 'div']:
                if temp_text:
                    result_text.append(temp_text)
                    temp_text = ""

    # Print each text string on a new line
    for text in result_text:
        print(text)

# Use the function on your HTML content.
html_content = """
<html>
<body>
    <b>This should not matter</b>
    <span><b>This shouldn't either</b></span>
    <audio src="audio.mp3"></audio>
    <div>
        <span><Text that should be included in the output</span>
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
