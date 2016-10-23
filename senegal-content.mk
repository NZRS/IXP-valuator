MSM_ID_FILE=senegal-to-local-content.txt
MSM_DATA_FILE=senegal-content-measurements.json
OUT_DATA_FILE=senegal-content-aggregated.json

all: ${OUT_DATA_FILE}

${MSM_DATA_FILE}: ${MSM_ID_FILE}
	python2 fetch-measurements.py --input ${MSM_ID_FILE} --output ${MSM_DATA_FILE}

${OUT_DATA_FILE}: ${MSM_DATA_FILE}
	python2 ixp-customer.py --msm-file ${MSM_DATA_FILE} \
		--network-file GeoLite2-Country.mmdb \
		--detection country \
		--country SN \
		--save-file ${OUT_DATA_FILE}
