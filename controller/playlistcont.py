from packages import sqliteconn



def song_remover(data,usernme):

    try:

        sqlitecon = sqliteconn.initconn()

        sqcursor = sqlitecon.cursor()

        sqcursor.execute("UPDATE tbl_userongs SET status = 1 WHERE username = (?) AND songid = (?)",(usernme,data["song_id"],))

        print("Status Updated")

    except Exception as e:

        print("Error is ",e)

    finally:
        sqlitecon.commit()
        sqcursor.close()
        sqlitecon.close()    
    