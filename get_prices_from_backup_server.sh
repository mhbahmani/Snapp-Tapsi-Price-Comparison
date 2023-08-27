#!/bin/bash

log_file="price_fetcher.logs"
# target_line="Timeout, Waiting..."
target_line="referenced before assignment"
target_line_2="Connection refused"

# Continuously monitor the log file
tail -F -n0 "$log_file" | while read -r line
do
	# Check if the target line is present
	if [[ "$line" == *"$target_line"* ]] || [[ "$line" == *"$target_line_2"* ]]; then
		echo "\"$line\" Fount. Performing price copy"

		ssh -l root dgocean-1 "cd /root/projects/price_com/; PYTHONUNBUFFERED=0 SCRAPE_INTERVAL=600 python3 /root/projects/price_com/price_fetcher.py | tee -a /root/projects/price_com/price_fetcher.logs"
		rsync -rP dgocean-1:/root/projects/price_com/prices.txt .
	fi
	sleep 1
done

