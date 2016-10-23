MSM_ID_FILE=sweden-msm-id.txt
MSM_DATA_FILE=sweden-results.json
OUT_DATA_FILE=sweden-content-aggregated.json

all: ${OUT_DATA_FILE}

${MSM_DATA_FILE}: ${MSM_ID_FILE}
	python2 fetch-measurements.py --input ${MSM_ID_FILE} --output ${MSM_DATA_FILE}

${OUT_DATA_FILE}: ${MSM_DATA_FILE} ixp-customer.py
	python2 ixp-customer.py --msm-file ${MSM_DATA_FILE} \
		--network-file peeringdb-dump.json \
		--detection IXP \
		--save-file ${OUT_DATA_FILE}


