#!/bin/bash

log_file="price_fetcher.logs"
# target_line="Timeout, Waiting..."
target_line="Use backup server"

# Continuously monitor the log file
tail -F -n0 "$log_file" | while read -r line
do
	# Check if the target line is present
	if [[ "$line" == *"$target_line"* ]]; then
		echo "\"$line\" Fount. Performing price copy"

		ssh -l root dgocean-1 "cd /root/projects/price_com/; RUN_ONCE=true PYTHONUNBUFFERED=0 SCRAPE_INTERVAL=600 python3 /root/projects/price_com/price_fetcher.py | tee -a /root/projects/price_com/price_fetcher.logs"
		rsync -rP dgocean-1:/root/projects/price_com/prices.txt .
	fi
	sleep 1
done

