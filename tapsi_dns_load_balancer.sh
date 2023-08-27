#!/bin/bash

log_file="price_fetcher.logs"
# target_line="Timeout, Waiting..."
target_line="TAPSI chitgarRight_chitgarUp_short"
target_line_2="Timeout, Waiting..."

CURRENT_IP_INDEX=0
DOMAIN="api.tapsi.cab"


IFS=$'\n' read -r -d '' -a ip_list < <( dig $DOMAIN | grep "api.tapsi.cab" | grep -Eo "([0-9]+\.){3}[0-9]+" && printf '\0' )


if ! grep -q "${DOMAIN}" /etc/hosts; then
	# Append the host record to /etc/hosts
	echo "Set the record for $DOMAIN"
        echo -e "${ip_list[0]}\t${DOMAIN}" | sudo tee -a /etc/hosts > /dev/null
fi

# Continuously monitor the log file
tail -F -n0 "$log_file" | while read -r line
do
	# Check if the target line is present
	if [[ "$line" == *"$target_line"* ]] || [[ "$line" == *"$target_line_2"* ]]; then
		echo "\"$line\" Fount. Performing dns change"
		CURRENT_IP_INDEX=$(( (CURRENT_IP_INDEX + 1) % ${#ip_list[@]} ))

		echo "${ip_list[CURRENT_IP_INDEX]}"
		sudo sed -i "/${DOMAIN}/c\\${ip_list[CURRENT_IP_INDEX]} $DOMAIN" /etc/hosts
	fi
done

