cd ../fuzz_checker
pipenv run python ./executor.py -b ../experiments/bin/objdump -c ../experiments/sym/bin/objdump -t ../angora_results/objdump/output/traces/ -o ../angora_results/objdump/results/