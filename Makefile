OUT_PATH=/usr/local/sbin
PIP_BIN=/usr/local/bin/pip3

OUT_FILE=$(OUT_PATH)/mmreplay

install:
	cp ./mmrelay.py $(OUT_FILE)
	$(PIP_BIN) install -r requirements.txt
	chmod 0755 $(OUT_FILE)