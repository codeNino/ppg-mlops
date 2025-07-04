from server import read_root

def test_read_root():
    assert read_root().get("message") ==  "Hello, World!"