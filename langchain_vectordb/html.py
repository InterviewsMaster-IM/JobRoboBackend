from bs4 import BeautifulSoup


def clean_html(html_string):
    # Parse the HTML string
    soup = BeautifulSoup(html_string, 'html.parser')

    # List of interactive elements to check
    interactive_elements = ['input', 'option', 'button', 'textarea', 'select']

    # Iterate over all elements
    for tag in soup.find_all():
        # If it's an interactive element
        if tag.name in interactive_elements:
            # Keep only the 'id' attribute if present
            attrs_to_keep = tag.attrs.get('id')
            tag.attrs.clear()
            if attrs_to_keep:
                tag.attrs['id'] = attrs_to_keep
        else:
            # If not interactive, remove all attributes
            tag.attrs.clear()

    # Return the modified HTML as a string
    return str(soup)
