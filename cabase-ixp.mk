MSM_ID_FILE=argentina-msm-id.txt
MSM_DATA_FILE=cabase-ixp-measurements.json
OUT_DATA_FILE=cabase-ixp-aggregated.json
NETWORK_FILE=cabase-networks.json

all: ${OUT_DATA_FILE}

${MSM_DATA_FILE}: ${MSM_ID_FILE}
	python2 fetch-measurements.py --input ${MSM_ID_FILE} --output ${MSM_DATA_FILE}

${OUT_DATA_FILE}: ${MSM_DATA_FILE} ixp-customer.py
	python2 ixp-customer.py --msm-file ${MSM_DATA_FILE} \
		--network-file ${NETWORK_FILE} \
		--detection customer \
		--save-file ${OUT_DATA_FILE}

