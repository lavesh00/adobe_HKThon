echo "Benchmarking Round 1A..."
time python run.py --mode 1a --input tests/test_data/sample.pdf --output /
tmp/out1a.json
echo "Benchmarking Round 1B..."
time python run.py --mode 1b --input tests/test_data/sample1.pdf tests/
test_data/sample2.pdf --persona "Sample persona description" --output /tmp/
out1b.json