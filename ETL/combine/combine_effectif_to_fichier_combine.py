import os
import pandas as pd


class FinalSortETL:
    """
    ETL process that:
      1. Extracts unique siren numbers from the template (renamed) file.
      2. Extracts matching rows from the effectif file.
      3. Merges the template data with the effectif data.
      4. Loads (saves) the final merged data to a CSV file.
    """

    def __init__(
        self,
        template_file: str,
        effectif_file: str,
        output_file: str,
        chunk_size: int = 100_000,
    ):
        """
        Initialize the ETL pipeline with file paths and chunk size.

        :param template_file: Path to the input template CSV file.
        :param effectif_file: Path to the input effectif CSV file.
        :param output_file: Path to the final output CSV file.
        :param chunk_size: Number of rows per chunk (default is 100,000).
        """
        self.template_file = template_file
        self.effectif_file = effectif_file
        self.output_file = output_file
        self.chunk_size = chunk_size

    def extract_template_siren_set(self) -> set:
        """
        Extract unique siren numbers from the template file.
        :return: A set of unique siren numbers (as integers).
        """
        siren_numbers = []
        # Count total lines (optional, for logging)
        with open(self.template_file, "r") as f:
            total_lines = sum(1 for _ in f) - 1  # subtract header
        print("Total lines in template file (excluding header):", total_lines)

        # Read template file in chunks to extract the 'siren_number' column
        for chunk in pd.read_csv(
            self.template_file,
            chunksize=self.chunk_size,
            delimiter=";",
            usecols=["siren_number"],
            low_memory=False,
            on_bad_lines="skip",
        ):
            # Drop NA and convert to numeric
            chunk = chunk.dropna(subset=["siren_number"])
            chunk["siren_number"] = pd.to_numeric(
                chunk["siren_number"], errors="coerce"
            )
            chunk = chunk.dropna(subset=["siren_number"])
            siren_numbers.extend(chunk["siren_number"].astype(int).tolist())

        siren_set = set(siren_numbers)
        print("Extracted", len(siren_set), "unique siren numbers from template.")
        return siren_set

    def extract_effectif_matches(self, siren_set: set) -> pd.DataFrame:
        """
        Read the effectif file in chunks and keep rows where the 'siren' column matches a value in siren_set.

        :param siren_set: A set of siren numbers to match.
        :return: A DataFrame with all matching effectif rows.
        """
        matched_chunks = []
        for chunk in pd.read_csv(
            self.effectif_file,
            chunksize=self.chunk_size,
            delimiter=";",
            low_memory=False,
        ):
            if "siren" in chunk.columns:
                # Convert the 'siren' column to numeric
                chunk["siren"] = pd.to_numeric(chunk["siren"], errors="coerce")
                matched_chunk = chunk[chunk["siren"].isin(siren_set)]
                if not matched_chunk.empty:
                    matched_chunks.append(matched_chunk)
            else:
                print("Warning: Column 'siren' not found in an effectif chunk.")
        if matched_chunks:
            matched_data = pd.concat(matched_chunks, ignore_index=True)
            print("Total matched effectif rows:", len(matched_data))
        else:
            matched_data = pd.DataFrame()
            print("No matched effectif data found.")
        return matched_data

    def merge_data(self, matched_effectif: pd.DataFrame) -> pd.DataFrame:
        """
        Merge the full template data with the matched effectif data on 'siren_number' and 'siren'.

        :param matched_effectif: DataFrame with effectif rows that match the template siren numbers.
        :return: Merged DataFrame.
        """
        # Load the full template data
        template_data = pd.read_csv(self.template_file, delimiter=";", low_memory=False)
        # Merge on left 'siren_number' and right 'siren'
        merged_data = template_data.merge(
            matched_effectif, left_on="siren_number", right_on="siren", how="left"
        )
        if "siren" in merged_data.columns:
            merged_data.drop("siren", axis=1, inplace=True)
        return merged_data

    def load(self, merged_data: pd.DataFrame):
        """
        Save the merged DataFrame to the output CSV file.

        :param merged_data: The final merged DataFrame.
        """
        # Ensure the output directory exists
        output_dir = os.path.dirname(self.output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        merged_data.to_csv(self.output_file, index=False, sep=";")
        print("Merging complete. Output saved to:", self.output_file)

    def run(self):
        """
        Run the full ETL pipeline.
        """
        siren_set = self.extract_template_siren_set()
        matched_effectif = self.extract_effectif_matches(siren_set)
        merged_data = self.merge_data(matched_effectif)
        self.load(merged_data)


if __name__ == "__main__":
    template_file = "./ETL/data/output/transform/fichier_combine.csv"
    effectif_file = "./ETL/data/output/extract/stock_unite_legale.csv"
    output_file = "./ETL/data/output/combine/fichier_effectif_and_combine.csv"

    etl_pipeline = FinalSortETL(
        template_file, effectif_file, output_file, chunk_size=100_000
    )
    etl_pipeline.run()
