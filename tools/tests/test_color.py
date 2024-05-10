from tools import Color 


def test_color():
    c = Color(3, 5, 6)
    assert c.rgb == (3, 5, 6), "Invalid rgb value"

    c = Color(256, 256, 256)
    assert c.rgb == (255, 255, 255), "Invalid rgb value"

    c1 = Color(255, 23, 156)
    c2 = Color(45, 243, 156)
    assert c1 + c2 == (255, 255, 255), "Invalid addition rgb result"
    assert c2 - c1 == (0, 220, 0), "Invalid subtraction rgb result"
