from tests.dbs import dbs

def test_chat(dbs):
    res = dbs.chat_query("nd","summarize the declaration of independence")
    print(str(res))