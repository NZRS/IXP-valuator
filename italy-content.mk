MSM_ID_FILE=italy-content-msm-id.txt
MSM_DATA_FILE=italy-content-measurements.json
OUT_DATA_FILE=italy-content-aggregated.json
COUNTRY=IT

all: ${OUT_DATA_FILE}

${MSM_DATA_FILE}: ${MSM_ID_FILE}
	python2 fetch-measurements.py --input ${MSM_ID_FILE} --output ${MSM_DATA_FILE}

${OUT_DATA_FILE}: ${MSM_DATA_FILE} ixp-customer.py
	python2 ixp-customer.py --msm-file ${MSM_DATA_FILE} \
		--network-file GeoLite2-Country.mmdb \
		--detection country \
		--country ${COUNTRY} \
		--save-file ${OUT_DATA_FILE}

