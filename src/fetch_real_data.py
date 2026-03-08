import glob
import os

from datasets import load_dataset

DATA_DIR = "data"


def fetch_mtsamples():
    print("Fetching high-end medical transcriptions dataset from HuggingFace...")
    try:
        # MTSamples contains realistic, anonymized medical transcriptions across various specialties
        dataset = load_dataset("NickyNicky/medical_mtsamples", split="train")
    except Exception as e:
        print(f"Error fetching dataset: {e}")
        return

    # Ensure directory exists and is clean
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    else:
        # Clean existing mock data to ensure we only use the high-end data
        for f in glob.glob(os.path.join(DATA_DIR, "*.txt")):
            try:
                os.remove(f)
            except Exception as e:
                print(f"Could not remove {f}: {e}")

    # Save a substantial subset (e.g., 250 records) for the vector store
    num_samples = min(250, len(dataset))
    print(
        f"Saving {num_samples} realistic patient medical transcripts to '{DATA_DIR}' directory..."
    )

    saved_count = 0
    for i in range(num_samples):
        record = dataset[i]
        transcription = record.get("transcription", "")
        specialty = record.get("medical_specialty", "General")
        description = record.get("description", "")

        # Skip empty transcriptions
        if not transcription or transcription.strip() == "":
            continue

        content = f"Patient Report ID: PT-10{i:03d}\n"
        content += f"Medical Specialty: {specialty.strip()}\n"
        content += f"Case Description: {description.strip()}\n\n"
        content += f"--- Clinical Transcription ---\n{transcription.strip()}\n"

        filepath = os.path.join(DATA_DIR, f"patient_10{i:03d}.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        saved_count += 1

    print(
        f"Successfully replaced dummy data with {saved_count} high-end clinical notes!"
    )


if __name__ == "__main__":
    fetch_mtsamples()
