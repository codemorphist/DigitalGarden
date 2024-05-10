from tools import Vector


def test_vec_operations():
    v1 = Vector(1, 2)
    v2 = Vector(2, 3)

    assert v1 + v2 == Vector(3, 5), "Invalid result of add vectors"
    assert v1 - v2 == Vector(-1, -1), "Invalid result of sub vectors"
    assert 2 * v1 == Vector(2, 4), "Invalid result of mul vector and int"
    assert v1 * 2 == Vector(2, 4), "Invalid result of mul vector and int"
    assert v1 / 3  == Vector(1/3, 2/3), "Invalid result of div vector by int"
    
