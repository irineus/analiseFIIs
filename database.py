import pandas
from pymongo import MongoClient
import passwords


def conecta_certificado(cliente):
    uri = "mongodb+srv://cluster0.u55rz.mongodb.net/Cluster0?authSource=%24external&authMechanism=MONGODB-X509" \
          "&retryWrites=true&w=majority "
    path = r'C:\Users\irineus\OneDrive\Documentos\Certificado MongoDB\X509-cert-6611857546994838642.pem'
    client = MongoClient(uri,
                         tls=True,
                         tlsCertificateKeyFile=path)
    db = client[cliente]
    return db


def conecta_usuario_senha(cliente):
    user = passwords.mongoDB_atlas['username']
    pwd = passwords.mongoDB_atlas['password']
    conn_str = f'mongodb+srv://{user}:{pwd}@cluster0.u55rz.mongodb.net/{cliente}?retryWrites=true&w=majority'
    client = MongoClient(conn_str)
    db = client[cliente]
    return db


def acessa_colecao(colecao, db):
    collection = db[colecao]
    # doc_count = collection.count_documents({})
    # print(doc_count)
    return collection


def inserir_df(colecao, df):
    # try:
    df_copy = pandas.DataFrame.copy(df)
    df_dict = df_copy.to_dict('records')
    colecao.insert_many(df_dict)
    # except:
    #     pass


def limpar_colecao(colecao):
    try:
        colecao.delete_many({})
    except:
        pass
