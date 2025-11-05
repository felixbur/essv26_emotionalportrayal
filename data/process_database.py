#!/usr/bin/env python3
"""
Process audio database files and create a pandas CSV with metadata.

This script reads audio files (WAV) and their corresponding transcription files (txt)
from the data folder and creates a CSV with extracted metadata including:
- file: audio file path (index)
- transcription: text content from .txt files
- speaker: extracted from filename (e.g., M_26 from G_1991_M_26_st.WAV)
- gender: extracted from filename (M = male, F = female)
- age: calculated from birth year (assuming current year is 2025)
"""

import os
import re
from pathlib import Path
from typing import Optional, Tuple

import pandas as pd


def parse_filename(
    filename: str,
) -> Tuple[Optional[str], Optional[str], Optional[int], Optional[int]]:
    """
    Parse filename to extract metadata.

    Expected format: G_YYYY_G_NN_st.WAV
    where YYYY is birth year, G is gender (M/F), NN is numeric ID

    Args:
        filename: Audio filename (e.g., "G_1991_M_26_st.WAV")

    Returns:
        Tuple of (speaker, gender, age, birth_year)
    """
    # Pattern: G_YYYY_G_NN_st.WAV or similar
    pattern = r"G_(\d{4})_([MF])_(\d+)_st\.(WAV|wav)"
    match = re.match(pattern, filename)

    if not match:
        return None, None, None, None

    birth_year = int(match.group(1))
    gender_code = match.group(2)
    id_number = match.group(3)

    # Create speaker ID
    speaker = f"{gender_code}_{id_number}"

    # Map gender code to full name
    gender = "male" if gender_code == "M" else "female"

    # Calculate age (assuming current year is 2025 as per context)
    current_year = 2025
    age = current_year - birth_year

    return speaker, gender, age, birth_year


def read_transcription(txt_path: Path) -> str:
    """
    Read transcription from text file.

    Args:
        txt_path: Path to transcription file

    Returns:
        Transcription text (stripped of extra whitespace)
    """
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        return content
    except Exception as e:
        print(f"Warning: Could not read {txt_path}: {e}")
        return ""


def process_database(data_folder: str = "data") -> pd.DataFrame:
    """
    Process all audio files in the data folder and create a dataframe.

    Args:
        data_folder: Path to folder containing audio and text files

    Returns:
        DataFrame with columns: file (index), transcription, speaker, gender, age, birth_year
    """
    data_path = Path(data_folder)

    if not data_path.exists():
        raise FileNotFoundError(f"Data folder not found: {data_folder}")

    # Find all audio files (both .WAV and .wav)
    audio_files = list(data_path.glob("*.WAV")) + list(data_path.glob("*.wav"))

    print(f"Found {len(audio_files)} audio files")

    records = []

    for audio_file in sorted(audio_files):
        filename = audio_file.name

        # Parse metadata from filename
        speaker, gender, age, birth_year = parse_filename(filename)

        if speaker is None:
            print(f"Warning: Could not parse filename: {filename}")
            continue

        # Find corresponding transcription file
        txt_file = audio_file.with_suffix(".txt")
        transcription = ""

        if txt_file.exists():
            transcription = read_transcription(txt_file)
        else:
            print(f"Warning: No transcription file found for {filename}")

        # Create record
        record = {
            "file": str(audio_file.relative_to(data_path.parent)),
            "speaker": speaker,
            "gender": gender,
            "age": age,
            "birth_year": birth_year,
            "transcription": transcription,
        }

        records.append(record)

    # Create dataframe
    df = pd.DataFrame(records)

    # add a dummy column for emotion to avoid errors in experiments
    df["emotion"] = "unknown"

    # Reorder columns to ensure transcription is last
    column_order = [
        "file",
        "speaker",
        "gender",
        "age",
        "birth_year",
        "emotion",
        "transcription",
    ]
    df = df[column_order]

    # Set file as index
    df.set_index("file", inplace=True)

    return df


def main():
    """Main execution function."""
    print("Processing database files...")

    # Process the database
    df = process_database("data")

    # Display summary
    print(f"\nProcessed {len(df)} files")
    print(f"\nDataFrame info:")
    print(df.info())
    print(f"\nFirst few rows:")
    print(df.head())
    print(f"\nSummary statistics:")
    print(df[["age", "gender"]].describe())
    print(f"\nGender distribution:")
    print(df["gender"].value_counts())

    # Save to CSV
    output_file = "metadata.csv"
    df.to_csv(output_file)
    print(f"\nSaved to {output_file}")


if __name__ == "__main__":
    main()
