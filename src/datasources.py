"""
    External data source.
    - data which need to need for context construction can be initialized here.
"""
import pandas as pd

class MedDataset:
    # A medical dataset 
    def __init__(self, path: str, batch_size: int=32, shuffle: bool=True):
        self.dataset_path = path
        self.batch_size = batch_size
        self.df = self._read_data()
        if shuffle:
            self.df = self.df.sample(frac=1).reset_index(drop=True)

    def _read_data(self):
        condition_dict = {
            0: "digestive system diseases",
            1: "cardiovascular diseases",
            2: "neoplasms",
            3: "nervous system diseases",
            4: "general pathological conditions"

        }
        df = pd.read_csv(self.dataset_path, sep='\t', header=None)

        df.rename(columns = {0: 'conditions', 1: 'record'}, inplace=True)
        df = df[df['conditions'] != 5]
        df['conditions']= df["conditions"].map(condition_dict)
        return df
    def __len__(self):
        return len(self.df)

    def __iter__(self):
        for i in range(0, len(self.df), self.batch_size):
            start = i
            end = min(start+self.batch_size, len(self.df))
            yield self.df.iloc[start:end]



# sanity checking the dataset.
if __name__ == "__main__":
    dataset = MedDataset(path="documents/train.dat")
    for batch in dataset:
        
        for i in batch.iterrows():
            print(i[1]['record'])
            break
            
        break