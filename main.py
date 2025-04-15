# import package
from fastapi import FastAPI, HTTPException, Header

import pandas as pd

password = "secret123"
# create FastAPI object
app = FastAPI()

# endpoint -> merupakan sebuah alamat yang mau kita tentukan untuk sebuah halaman. Atau bisa dibilang merupakan halaman tertentu yang bisa diakses client
# create endpoint untuk mndapatkan data di halaman awal/utama


@app.get("/home")
def getData():  # function handler, tujuannya untuk menghandle request dari endpoint tertentu.
    return {
        "message": "hello world !!!"
    }


@app.get("/home/data")
def getCSV():  # function handler, tujuannya untuk menghandle request dari endpoint tertentu.

    # 1. baca data dari csv
    df = pd.read_csv("data.csv")

    # 2. tampilkan response beruta data csv menjadi json.
    # diubah karena datafreame dan json beda format. diubah ke dict karena json = dict
    # supaya bentuk tampilan di websitenya lebih rapih
    return df.to_dict(orient="records")


@app.get("/home/data/{name}")
# function handler, tujuannya untuk menghandle request dari endpoint tertentu.
def getDataByName(name: str):

    # 1. baca data dari csv
    df = pd.read_csv("data.csv")

    # 2. Filter data by name.
    result = df[df['name'] == name]

    # check apakah hasil filternya ada atau > 0

    if len(result) > 0:

        # 3. Tampilkan data response berupa rsult
        return result.to_dict(orient="records")
    else:
        # tampilkan pesan error
        # klo nampilin pesan error harus pake raise
        raise HTTPException(
            status_code=404, detail="data" + name + "tidak ditemukan")


# delete data yang ada di csv

@app.delete("/home/data/{name}")
# function handler, tujuannya untuk menghandle request dari endpoint tertentu.
def deleteDataByName(name: str, api_key: str = Header(None)):
    # cek autentifikasinya.
    if api_key != None and api_key == password:

        # 1. baca data dari csv
        df = pd.read_csv("data.csv")

        # 2. Filter data by name.
        result = df[~(df['name'] == name)]

        # .3 repcalse data existing -> data yang dimasukkan berdasarkan filter
        result.to_csv('data.csv', index=False)

        # 4. Tampilkan data response berupa rsult
        return result.to_dict(orient="records")

    else:
        raise HTTPException(status_code=403, detail="Password Salah")
