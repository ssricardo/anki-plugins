# Initial version

providers = {
    'Google Web': 'https://google.com/search?q={}',
    'Google Images': 'https://www.google.com/search?tbm=isch&q={}'
}

from anki_web_browser.controller import run

run(providers)