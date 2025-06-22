import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

class DataLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None

    def load_data(self):
        try:
            self.data = pd.read_csv(self.filepath)
            print("Data loaded successfully.")
        except FileNotFoundError:
            print(f"Error: '{self.filepath}' not found.")
            self.data = None
        except Exception as e:
            print(f"An error occurred: {e}")
            self.data = None

class DataManager:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def show_overview(self):
        if self.data is not None:
            print("\nFirst 5 rows:")
            print(self.data.head())
            print("\nData summary:")
            print(self.data.describe(include='all'))
            print("\nMissing values per column:")
            print(self.data.isnull().sum())
        else:
            print("No data to display.")

    def show_info(self):
        if self.data is not None:
            print("\nData Info:")
            print(self.data.info())
        else:
            print("No data to display.")
    def clean_data(self):
        if self.data is not None:
            # Example: fill numeric NaNs with median, categorical with mode
            for col in self.data.columns:
                if self.data[col].dtype in ['float64', 'int64']:
                    self.data[col].fillna(self.data[col].median(), inplace=True)
                else:
                    self.data[col].fillna(self.data[col].mode()[0], inplace=True)
            print("Missing values filled.")
        else:
            print("No data to clean.")

    def select_columns(self, columns):
        if self.data is not None:
            selected = self.data[columns]
            print(f"\nSelected columns: {columns}")
            print(selected.head())
            return selected
        else:
            print("No data to select from.")
            return None

    def save_data(self, output_path, file_format='excel', overwrite=True, append=False):
        if self.data is not None:
            # Determine file extension
            if file_format == 'excel':
                if not output_path.lower().endswith('.xlsx'):
                    output_path += '.xlsx'
            elif file_format == 'csv':
                if not output_path.lower().endswith('.csv'):
                    output_path += '.csv'
            else:
                print("Unsupported file format.")
                return

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            try:
                if file_format == 'excel':
                    if not overwrite and os.path.exists(output_path):
                        print(f"File {output_path} already exists. Set overwrite=True to replace it.")
                        return
                    self.data.to_excel(output_path, index=False)
                    print(f"Data saved to {output_path} (Excel format).")
                elif file_format == 'csv':
                    if append and os.path.exists(output_path):
                        self.data.to_csv(output_path, mode='a', header=False, index=False)
                        print(f"Data appended to {output_path} (CSV format).")
                    else:
                        if not overwrite and os.path.exists(output_path):
                            print(f"File {output_path} already exists. Set overwrite=True to replace it.")
                            return
                        self.data.to_csv(output_path, index=False)
                        print(f"Data saved to {output_path} (CSV format).")
            except Exception as e:
                print(f"Failed to save data: {e}")
        else:
            print("No data to save.")

    def visualize_data(self):
        if self.data is not None:
            numeric_cols = self.data.select_dtypes(include=['float64', 'int64']).columns
            categorical_cols = self.data.select_dtypes(include=['object', 'category']).columns
            if len(numeric_cols) > 0:
                self.data[numeric_cols].hist(bins=20, figsize=(12, 8))
                plt.suptitle('Histograms of Numeric Columns')
                plt.show()
            if len(categorical_cols) > 0:
                for col in categorical_cols:
                    plt.figure(figsize=(8, 4))
                    self.data[col].value_counts().head(10).plot(kind='bar')
                    plt.title(f'Top 10 Categories in {col}')
                    plt.xlabel(col)
                    plt.ylabel('Count')
                    plt.show()
            if len(numeric_cols) > 1:
                plt.figure(figsize=(10, 8))
                sns.heatmap(self.data[numeric_cols].corr(), annot=True, cmap='coolwarm')
                plt.title('Correlation Heatmap')
                plt.show()
        else:
            print("No data to visualize.")

class SignInSystem:
    def __init__(self):
        # For demo: hardcoded credentials. In production, use secure storage.
        self.valid_users = {'admin': 'password123', 'user': 'testpass'}

    def sign_in(self):
        print("=== Sign In ===")
        username = input("Username: ")
        password = input("Password: ")
        if username in self.valid_users and self.valid_users[username] == password:
            print("Sign-in successful!\n")
            return True
        else:
            print("Invalid username or password. Exiting.")
            return False

def main():
    signin = SignInSystem()
    if not signin.sign_in():
        return
    loader = DataLoader('amazon_delivery.csv')
    loader.load_data()
    if loader.data is not None:
        manager = DataManager(loader.data)
        manager.show_overview()
        manager.show_info()
        manager.clean_data()
        manager.show_overview()
        # Data visualization
        manager.visualize_data()
        # Example: select specific columns if needed
        # manager.select_columns(['column1', 'column2'])
        # Save cleaned data to output folder in Excel format
        manager.save_data(
            output_path=os.path.join('output', 'amazon_delivery_cleaned.xlsx'),
            file_format='excel'
        )

if __name__ == "__main__":
    main()
