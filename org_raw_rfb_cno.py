import os 
import time
import requests, zipfile
# import wget
import shutil
import pandas as pd
import glob
import concurrent.futures
from concurrent.futures import as_completed

from azure.storage.filedatalake import FileSystemClient

from core.bot import initialize, log_status
from core.adls import drop_directory, upload_file


def extract_all_zip(path, file_name) -> None:
    # ,remover=True
    with zipfile.ZipFile(path + file_name, "r") as z:
        z.extractall(path)
    return time.sleep(10)


#        time.sleep(10)
#        if remover == True:
#            print("Deleted '%s' directory successfully" % path)
#        else:
#            raise Exception(f'status_code not 200.')


def make_headers(start, chunk_size):
    end = start + chunk_size - 1
    return {"Range": f"bytes={start}-{end}"}


def __delete_file():
    test = os.listdir("././.")
    for item in test:
        if item.endswith(".tmp"):
            ## print(item)
            os.remove(item)

    # {lnd}/{schema}{table}


def iter(url, file_name, chunk_size):
    response = requests.get(url, stream=True)
    file_size = int(response.headers.get("content-length", 0))
    chunk_size = chunk_size
    chunks = range(0, file_size, chunk_size)
    my_iter = []
    for i, chunk in enumerate(chunks):
        start = chunk
        end = start + chunk_size - 1
        make_headers = {"Range": f"bytes={start}-{end}"}
        my_iter.append([url, make_headers, f"{file_name}.part{i}"])
    return my_iter


def download_part(tmp, chunk_size, url_and_headers_and_partfile):
    url, headers, partfile = url_and_headers_and_partfile
    response = requests.get(url, headers=headers)
    size = 0
    with open(tmp + partfile, "wb") as f:
        for chunk in response.iter_content(chunk_size):
            if chunk:
                size += f.write(chunk)
    print(size)
    if size == chunk_size:
        print("chunk_size == ", chunk_size)
    else:
        print("chunk_size !=")
        return download_part(tmp, chunk_size, url_and_headers_and_partfile)


def download_part_(tmp, chunk_size, url_and_headers_and_partfile):
    url, headers, partfile = url_and_headers_and_partfile
    response = requests.get(url, headers=headers)
    size = 0
    with open(tmp + partfile, "wb") as f:
        for chunk in response.iter_content(chunk_size):
            if chunk:
                size += f.write(chunk)
    return size


def main(**kwargs):
    bot = initialize()
    LND: str = bot.lnd
    adl: FileSystemClient = bot.adl

    url = "http://200.152.38.155/CNO/cno.zip"
    file_name = "cno"

    schema = "rfb_cno"
    table = "cadastro_nacional_de_obras"
    # year = None
    tmp = "/tmp/org_raw_rfb_cno/"
    # tmp = 'C:/Users/acessocni01/Desktop/Test/file_/'
    chunk_size = 15000000
    os.makedirs(tmp, mode=0o777, exist_ok=True)
    try:
        start = time.time()
        my_iter_ = iter(url, file_name, chunk_size)
        my_iter_ = my_iter_[0:-1]
        my_iter__ = iter(url, file_name, chunk_size)
        my_iter__ = my_iter__[-1]

        download_part_(tmp, chunk_size, my_iter__)
        with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
            jobs = [
                executor.submit(download_part, tmp, chunk_size, i) for i in my_iter_
            ]
            for job in as_completed(jobs):
                size = job.result()

        end = time.time()
        print(end - start)

        response = requests.get(url, stream=True)
        file_size = int(response.headers.get("content-length", 0))
        chunk_size = chunk_size
        chunks = range(0, file_size, chunk_size)

        with open(tmp + file_name, "wb") as outfile:
            for i in range(len(chunks)):
                chunk_path = tmp + f"{file_name}.part{i}"
                with open(chunk_path, "rb") as s:
                    outfile.write(s.read())
                os.remove(chunk_path)

        extract_all_zip(tmp, file_name)
        # ,remover=True
        # shutil.rmtree('path', ignore_errors=True)

        # download_file(URL,tmp,remover=True)
        folder_path = tmp
        file_list = glob.glob(folder_path + "/*.csv")
        # print(file_list)
        file_list_url = [i for i in range(0, len(file_list))]
        # print(file_list_url)

        for n, i in zip(file_list, file_list_url):
            nome_inserido_durante_save = n.split("/")[-1].split("\\")[-1].split(".")[0]
            ## print(nome_inserido_durante_save)

            drop_directory(
                LND, adl, schema, table=table, year=nome_inserido_durante_save
            )
            ## print(file_list[i])
            data = pd.read_csv(file_list[i], encoding="ISO-8859-1")
            data["date"] = pd.to_datetime("today").strftime(
                "%d/%m/%Y"
            )  # .strftime("%m/%d/%Y")
            all_columns = list(data.columns)  # Creates list of all column headers
            data[all_columns] = data[all_columns].astype(str)

            #######################################################data.to_parquet('my.parquet', index=False)
            parquet_output = file_list[i].replace(
                ".csv", ".parquet"
            )  # /tmp/org_raw_rfb_cno/cno.csv
            ## print(parquet_output)
            ########################################################data.to_csv(parquet_output, index=False)
            data.to_parquet(parquet_output, index=False)
            upload_file(
                LND,
                adl,
                schema,
                table=table,
                year=nome_inserido_durante_save,
                file=parquet_output,
            )
        log_status("ok")
        return
    except Exception as e:
        raise e
    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    main(**kwargs)
