import requests
import os
from os.path import join
from pathlib import Path


class HelperDcmWeb():
    pacs_dcmweb = "http://dcm4chee-service.store.svc:8080/dcm4chee-arc/aets/KAAPANA"

    @staticmethod
    def downloadSeries(seriesUID, target_dir, include_series_dir=False):
        payload = {
            'SeriesInstanceUID': seriesUID
        }
        url = HelperDcmWeb.pacs_dcmweb + "/rs/instances"
        httpResponse = requests.get(url, params=payload)
        # print(f"Requesting URL: {url}")
        # print(f"httpResponse: {httpResponse}")
        # print(f"payload: {payload}")
        if httpResponse.status_code == 204:
            print("No results from pacs...")
            print("Can't request series!")
            return False
        elif httpResponse.status_code == 200:
            response = httpResponse.json()
            print(("Collecting objects for series {0}".format(seriesUID)))
            objectUIDList = []
            for resultObject in response:
                objectUIDList.append(
                    [
                        resultObject["0020000D"]["Value"][0],
                        resultObject["00080018"]["Value"][0]
                    ]
                )  # objectUID

            print(("Start downloading series: {0}".format(seriesUID)))
            if include_series_dir:
                target_dir = join(target_dir, seriesUID)
            Path(target_dir).mkdir(parents=True, exist_ok=True)
            for objectUID in objectUIDList:
                studyUID = objectUID[0]
                objectUID = objectUID[1]
                HelperDcmWeb.downloadObject(
                    studyUID=studyUID,
                    seriesUID=seriesUID,
                    objectUID=objectUID,
                    target_dir=target_dir
                )
            print("Done.")
            return True
        else:
            print("Error at PACS request!")
            return False

    @ staticmethod
    def downloadObject(studyUID, seriesUID, objectUID, target_dir):
        payload = {
            'requestType': 'WADO',
            'studyUID': studyUID,
            'seriesUID': seriesUID,
            'objectUID': objectUID,
            'contentType': 'application/dicom'
        }
        url = HelperDcmWeb.pacs_dcmweb + "/wado"
        response = requests.get(url, params=payload)
        fileName = objectUID+".dcm"
        filePath = os.path.join(target_dir, fileName)
        with open(filePath, "wb") as f:
            f.write(response.content)
