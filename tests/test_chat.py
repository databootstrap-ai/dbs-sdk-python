from databootstrap import DataBootstrap


def test_chat():
    dbs = DataBootstrap(email="", password="")
    res = dbs.chat_query("biorxiv","<question>")
    print(str(res))