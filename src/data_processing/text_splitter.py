# src/data_processing/text_splitter.py

import argparse
import os
import sys

# Adjust sys.path to ensure all internal modules are accessible
project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Points to the root of the project
sys.path.append(project_directory)

from src.utils.chunker import process_directory, save_splits_with_metadata

def main():
    parser = argparse.ArgumentParser(description="Process JSON and PDF files to split text.")
    parser.add_argument('--type', choices=['pdf', 'json', 'all'], default='all',
                        help='Specify the type of files to process: pdf, json, or all (default: all)')
    parser.add_argument('--json_dir', default='/usr/src/app/data/processed/json_files',
                        help='Directory path for JSON files')
    parser.add_argument('--pdf_dir', default='/usr/src/app/data/processed/pdf_files',
                        help='Directory path for PDF files')
    parser.add_argument('--doc_dir', default='/usr/src/app/data/processed/doc_files',
                        help='Directory path for DOC files')
    parser.add_argument('--output_dir', default='/usr/src/app/data/processed/splits_with_meta',
                        help='Output directory for split documents')
    parser.add_argument('--log_file', default='/usr/src/app/data/logs/skipped_files.log',
                        help='Log file path for recording skipped files')
    parser.add_argument('--id_log_path', default='/usr/src/app/data/logs/id_log.log',
                        help='Log file path for unique ID generation')

    args = parser.parse_args()

    # Ensure the output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    if args.type in ['json', 'all']:
        # Process JSON files
        json_splits_with_metadata = process_directory(args.json_dir, args.log_file, None)
        save_splits_with_metadata(json_splits_with_metadata, args.output_dir)

    if args.type in ['pdf', 'all']:
        # Process PDF files
        pdf_splits_with_metadata = process_directory(args.pdf_dir, args.log_file, args.id_log_path)
        save_splits_with_metadata(pdf_splits_with_metadata, args.output_dir)

if __name__ == '__main__':
    main()
