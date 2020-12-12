import utils

def test_extract_url():
    assert utils.extract_url(['https://asdf.dd']) == 'https://asdf.dd'    
