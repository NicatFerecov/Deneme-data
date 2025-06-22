import pandas as pd
import os

class DataLoader:
    """
    Advanced DataLoader for loading, inspecting, cleaning, and saving tabular data.

    Attributes:
        filepath (str): Path to the data file.
        data (pd.DataFrame): Loaded data.
    """

    def __init__(self, filepath):
        """
        Initialize DataLoader with the path to the data file.
        """
        self.filepath = filepath
        self.data = None

    def load(self, file_type='csv', **kwargs):
        """
        Load data from a file. Supports CSV and Excel.

        Args:
            file_type (str): 'csv' or 'excel'.
            **kwargs: Additional arguments for pandas read functions.
        """
        try:
            if file_type == 'csv':
                self.data = pd.read_csv(self.filepath, **kwargs)
            elif file_type == 'excel':
                self.data = pd.read_excel(self.filepath, **kwargs)
            else:
                raise ValueError("Unsupported file type.")
            print(f"Data loaded from {self.filepath}.")
        except Exception as e:
            print(f"Failed to load data: {e}")
            self.data = None

    def info(self):
        """
        Print info about the DataFrame.
        """
        if self.data is not None:
            print(self.data.info())
        else:
            print("No data loaded.")

    def overview(self, rows=5):
        """
        Print a quick overview of the data.

        Args:
            rows (int): Number of rows to show.
        """
        if self.data is not None:
            print(self.data.head(rows))
            print(self.data.describe(include='all'))
            print("Missing values per column:")
            print(self.data.isnull().sum())
        else:
            print("No data loaded.")

    def clean(self, strategy='auto'):
        """
        Clean missing values in the data.

        Args:
            strategy (str): 'auto' (numeric: median, categorical: mode), or 'drop' to drop rows with missing values.
        """
        if self.data is not None:
            if strategy == 'auto':
                for col in self.data.columns:
                    if self.data[col].dtype in ['float64', 'int64']:
                        self.data[col] = self.data[col].fillna(self.data[col].median())
                    else:
                        self.data[col] = self.data[col].fillna(self.data[col].mode()[0])
                print("Missing values filled (auto strategy).")
            elif strategy == 'drop':
                self.data.dropna(inplace=True)
                print("Rows with missing values dropped.")
            else:
                print("Unknown cleaning strategy.")
        else:
            print("No data loaded.")

    def select(self, columns):
        """
        Return a DataFrame with only the specified columns.

        Args:
            columns (list): List of column names to select.

        Returns:
            pd.DataFrame: Selected columns.
        """
        if self.data is not None:
            return self.data[columns]
        print("No data loaded.")
        return None

    def save(self, output_path, file_type='excel'):
        """
        Save the data to a file.

        Args:
            output_path (str): Path to save the file.
            file_type (str): 'excel' or 'csv'.
        """
        if self.data is not None:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            if file_type == 'excel':
                self.data.to_excel(output_path, index=False)
                print(f"Data saved to {output_path} (Excel format).")
            elif file_type == 'csv':
                self.data.to_csv(output_path, index=False)
                print(f"Data saved to {output_path} (CSV format).")
            else:
                print("Unsupported file type.")
        else:
            print("No data to save.")

# Example usage:
loader = DataLoader('amazon_delivery.csv')
loader.load()
loader.info()
loader.overview()
loader.clean()
loader.save('output/amazon_delivery_cleaned.xlsx', file_type='excel')
