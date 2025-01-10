from bs4 import BeautifulSoup
from pathlib import Path


def add_require_timeout(html_file):
    """ Add a timeout for the require's javascript library """
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')

    # Check if require.min.js is present
    is_require_loaded = any(
        script.get('src') and 'require.min.js' in script['src']
        for script in soup.find_all('script')
    )

    if not is_require_loaded:
        return

    new_script = soup.new_tag('script')
    new_script.string = """
        require.config({
            waitSeconds: 60
        });
    """

    if soup.head:
        soup.head.append(new_script)
    elif soup.body:
        soup.body.append(new_script)
    else:
        soup.append(new_script)

    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))


if __name__ == '__main__':
    html_folder = Path('html')
    html_files = [f.resolve() for f in html_folder.glob('*.html')]
    for html_file in html_files:
        add_require_timeout(html_file)
