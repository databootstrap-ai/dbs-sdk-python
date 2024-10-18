from tests.dbs import dbs

def test_search(dbs):
    res = dbs.search_query("nd","declaration of independence")
    print(str(res))