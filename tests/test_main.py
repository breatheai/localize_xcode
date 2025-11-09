from src.main import Localize

def test_hello_world():
    localize = Localize("./Localizable.xcstrings")
    localize.edit_xcstrings() # "../Localizable.xcstrings"
