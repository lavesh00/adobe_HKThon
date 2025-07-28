import argparse
import sys
import logging

from src.round1a_processor import Round1AProcessor
from src.round1b_processor import Round1BProcessor
from monitoring.performance_tracker import PerformanceTracker

# Initialize logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

def main():
    parser = argparse.ArgumentParser(description='Adobe Hackathon - PDF Intelligence Engine')
    parser.add_argument('--mode', type=str, choices=['1a', '1b'], required=True,
                        help='Mode of operation: 1a for PDF->JSON, 1b for multi-PDF analysis')
    parser.add_argument('--input', type=str, nargs='+', help='Input PDF file(s)')
    parser.add_argument('--persona', type=str, help='Persona description text (required for mode 1b)')
    parser.add_argument('--output', type=str, help='Output JSON file path')
    parser.add_argument('--job', type=str, default="AUTO-GENERATED", help='Optional: job to be done (used in metadata)')
    args = parser.parse_args()

    if args.mode == '1a':
        if not args.input or len(args.input) != 1 or not args.output:
            logging.error("Mode 1a requires exactly one input PDF and an output path.")
            sys.exit(1)
        with PerformanceTracker():
            processor = Round1AProcessor()
            processor.process(args.input[0], args.output)

    elif args.mode == '1b':
        if not args.input or not args.output or not args.persona:
            logging.error("Mode 1b requires --input PDFs --persona TEXT --output JSON.")
            sys.exit(1)
        with PerformanceTracker():
            processor = Round1BProcessor()
            processor.process(args.input, args.persona, args.output, args.job)

if __name__ == "__main__":
    main()