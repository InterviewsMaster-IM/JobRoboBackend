from bs4 import Comment
from bs4 import BeautifulSoup


def clean_html(html_string):
    # Parse the HTML string
    soup = BeautifulSoup(html_string, 'html.parser')

    # List of interactive elements to check
    interactive_elements = ['input', 'button', 'textarea', 'select', 'label']

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


def extract_interactive_elements(html_string):
    # Parse the HTML string
    soup = BeautifulSoup(html_string, 'html.parser')

    # List of interactive elements to check
    interactive_elements = ['input', 'button', 'textarea', 'select', 'label']

    # Find all interactive elements
    interactive_tags = soup.find_all(interactive_elements)

    # Create a new soup object to hold the interactive elements
    new_soup = BeautifulSoup('', 'html.parser')

    # Iterate over all interactive elements and append them to the new soup
    for tag in interactive_tags:
        new_soup.append(tag)

    # Return the modified HTML as a string containing only interactive elements
    return str(new_soup)


def reduce_tokens(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')

    # Initialize dictionaries to store unique class names and ids
    class_dict = {}
    id_dict = {}
    class_index = 0
    id_index = 0

    # Iterate over all elements with 'class', 'id', or 'for' attributes
    for tag in soup.find_all(lambda tag: 'class' in tag.attrs or 'id' in tag.attrs or 'for' in tag.attrs):
        # Replace class names with 'c{index}'
        if 'class' in tag.attrs:
            class_names = tag['class']
            for i, class_name in enumerate(class_names):
                if class_name not in class_dict:
                    class_dict[class_name] = f'c{class_index}'
                    class_index += 1
                # Replace the class name with 'c{index}'
                class_names[i] = class_dict[class_name]

        # Replace id with 'i{index}'
        if 'id' in tag.attrs:
            id_value = tag['id']
            if id_value not in id_dict:
                id_dict[id_value] = f'i{id_index}'
                id_index += 1
            # Replace the id with 'i{index}'
            tag['id'] = id_dict[id_value]

    # Iterate again for 'for' attributes to ensure all ids have been indexed
    for tag in soup.find_all(lambda tag: 'for' in tag.attrs):
        for_value = tag['for']
        if for_value in id_dict:
            # Replace the 'for' attribute with the corresponding 'i{index}'
            tag['for'] = id_dict[for_value]
        else:
            # If the 'for' attribute is not in id_dict, it's an error
            # Handle it according to your error policy (e.g., raise an exception, log a warning, etc.)
            pass

    # Return the modified HTML as a string
    return str(soup)


def clean_html_2(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')

    attributes_to_remove = ['aria-describedby', 'style',
                            'onclick', 'onmouseover', 'onmouseout', 'data-*', 'class']

    for tag in soup.find_all():
        for attribute in attributes_to_remove:
            if attribute.endswith('*'):
                prefix = attribute[:-1]
                for attr in list(tag.attrs):
                    if attr.startswith(prefix):
                        del tag.attrs[attr]
            elif attribute in tag.attrs:
                del tag.attrs[attribute]

    # Remove comments
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    return str(soup)
