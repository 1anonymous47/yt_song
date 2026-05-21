import pymongo


try:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = myclient["yt_player"]

    data_coll = mydb["data_records"]

except Exception as e:
    
    print("Mongo DB CONNECTION ERROR ",e)



