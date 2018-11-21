import pandas as pd


class fusion:
    def __init__(self, imported_files, start_hist, end_hist):
        self.files_repertories = imported_files  # Imported files repertories
        self.data = {}
        self.start_hist = start_hist
        self.end_hist = end_hist
        self.__loading()

    def __loading(self):
        print(self.files_repertories.values)

        for key, value in self.files_repertories.items():
            try:
                self.data[key] = pd.read_csv(value, error_bad_lines=False, sep="|", low_memory=False)
            except:
                raise Exception('an error occur during the loading of the csv files')

    def data_preparation(self):
        i = 0
        for dataframe in self.data.values():
            print(dataframe.columns)
            dataframe[self.end_hist] = dataframe[self.end_hist].replace('31/12/2999',
                                                                        '31/12/2100')  # replace out of range dates for a datetime format by acceptable ones
            dataframe[self.end_hist] = dataframe[self.end_hist].apply(
                lambda x: str(x[6:10]) + '/' + str(x[3:5]) + '/' + str(x[0:2]))  # Change euro format date to us format
            dataframe[self.start_hist] = dataframe[self.start_hist].apply(
                lambda x: str(x[6:10]) + '/' + str(x[3:5]) + '/' + str(x[0:2]))  # Change euro format date to us format
            dataframe[self.end_hist] = pd.to_datetime(dataframe[self.end_hist])  # Conversion to datetime format
            dataframe[self.start_hist] = pd.to_datetime((dataframe[self.start_hist]))  # Conversion to datetime format

            col = []  # Replace space to "_" to prepare the futur SQL operation
            for val in dataframe.columns:
                val = str(val).replace(" ", "_")
                col.append(val)

            dataframe.columns = col
            print(dataframe.dtypes)
        self.start_hist = str(self.start_hist).replace(" ", "_")
        self.end_hist = str(self.end_hist).replace(" ", "_")


a = fusion(imported_files={"contrat_02": r"C:\Users\Sabri\Desktop\CONTRAT_02.TXT",
                           "contrat_01": r"C:\Users\Sabri\Desktop\CONTRAT_01.TXT"}, start_hist="Start Date",
           end_hist="End Date")
a.data_preparation()