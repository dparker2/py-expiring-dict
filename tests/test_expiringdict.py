from expiring_dict import ExpiringDict
from time import sleep


def test_init():
    ExpiringDict()


def test_no_ttl():
    d = ExpiringDict()
    d["key"] = "value"
    assert len(d._ExpiringDict__keys) == 0


def test_class_ttl():
    d = ExpiringDict(ttl=0.01, interval=0.005)
    d["key"] = "should be gone"
    assert len(d) == 1
    sleep(0.02)
    assert len(d) == 0


def test_set_ttl():
    d = ExpiringDict(interval=0.005)
    d.ttl("key", "expire", 0.01)
    assert len(d) == 1
    sleep(0.02)
    assert len(d) == 0


def test_dict_ops():
    ed = ExpiringDict()
    ed["one"] = 1
    ed["two"] = 2
    ed["three"] = 3
    d = dict()
    d["one"] = 1
    d["two"] = 2
    d["three"] = 3
    assert [x for x in d] == [x for x in ed]
    assert [k for k in d.keys()] == [k for k in ed.keys()]
    assert [v for v in d.values()] == [v for v in ed.values()]
    assert [i for i in d.items()] == [i for i in ed.items()]
    assert "one" in ed


def test_class_ttl_twice():
    d = ExpiringDict(ttl=0.01, interval=0.005)
    d["key"] = "should be gone"
    assert len(d) == 1
    sleep(0.006)
    assert len(d) == 1
    sleep(0.02)
    assert len(d) == 0
    d["key"] = "should be gone"
    assert len(d) == 1
    sleep(0.006)
    assert len(d) == 1
    sleep(0.02)
    assert len(d) == 0


def test_class_reset_ttl_with_reinsert():
    d = ExpiringDict(ttl=0.01, interval=0.001)
    d["key"] = "should be reset"
    assert len(d) == 1
    sleep(0.006)
    assert len(d) == 1
    d["key"] = "should be reset"
    sleep(0.006)
    assert len(d) == 1
    sleep(0.006)
    assert len(d) == 0

    
def test_class_ttl_reinsert_after_delete():
    d = ExpiringDict(ttl=0.01, interval=0.005)
    d["key"] = "should be gone"
    assert len(d) == 1
    sleep(0.006)
    assert len(d) == 1
    del d["key"]
    assert len(d) == 0
    sleep(0.02)
    assert len(d) == 0
    d["key"] = "should be gone"
    assert len(d) == 1
    sleep(0.006)
    assert len(d) == 1
    sleep(0.02)
    assert len(d) == 0
