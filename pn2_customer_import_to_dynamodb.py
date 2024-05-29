from file_manager import FileManager

class Pn2CustomerImportToDynamodb:
    def __init__(self, csv_file_path, file_name, table_name, region_name, bucket):
        self.file_manager = FileManager(csv_file_path, file_name, region_name, table_name, bucket)

    def call(self):
        self.file_manager.move_files_to_Dynamodb()