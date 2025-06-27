#!/usr/bin/env python3
import csv
import json
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Convert CSV to JSONL')
    parser.add_argument('input_csv', help='Path to the input CSV file')
    parser.add_argument('output_jsonl', help='Path to the output JSONL file')
    return parser.parse_args()


def main():
    args = parse_args()
    with open(args.input_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        with open(args.output_jsonl, 'w', encoding='utf-8') as jsonlfile:
            for row in reader:
                jsonlfile.write(json.dumps(row, ensure_ascii=False))
                jsonlfile.write('\n')


if __name__ == '__main__':
    main()
