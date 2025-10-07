import pandas as pd
import random

def split_dataset():
    # Read the complete metadata
    complete_metadata_path = 'tests/te/metadata/complete_metadata.csv'
    df = pd.read_csv(complete_metadata_path)
    
    # Shuffle the dataframe
    df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Split into train (90%) and validation (10%)
    split_index = int(0.9 * len(df_shuffled))
    train_df = df_shuffled[:split_index]
    val_df = df_shuffled[split_index:]
    
    # Save train and validation metadata
    train_df.to_csv('tests/te/metadata/train_metadata.csv', index=False)
    val_df.to_csv('tests/te/metadata/val_metadata.csv', index=False)
    
    # Print statistics
    print(f"Total samples: {len(df_shuffled)}")
    print(f"Training samples: {len(train_df)} ({len(train_df)/len(df_shuffled)*100:.1f}%)")
    print(f"Validation samples: {len(val_df)} ({len(val_df)/len(df_shuffled)*100:.1f}%)")
    
    # Show sample entries from each set
    print("\nSample training entries:")
    for i, (_, row) in enumerate(train_df.head(3).iterrows()):
        print(f"  {row['file_name']}: {row['text'][:50]}{'...' if len(row['text']) > 50 else ''}")
    
    print("\nSample validation entries:")
    for i, (_, row) in enumerate(val_df.head(3).iterrows()):
        print(f"  {row['file_name']}: {row['text'][:50]}{'...' if len(row['text']) > 50 else ''}")

def main():
    print("Splitting dataset into train and validation sets...")
    split_dataset()
    print("Dataset split completed!")

if __name__ == "__main__":
    main()