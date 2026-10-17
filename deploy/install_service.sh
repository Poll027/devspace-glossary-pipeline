#!/usr/bin/env bash
# Install the supervisor as a systemd service on the EC2 instance. Run from the repo root:
#   export AWS_REGION=us-east-1 MAX_USD=300 SNS_TOPIC_ARN=arn:aws:sns:...:glossary-driver
#   bash deploy/install_service.sh batches/<batch_id>
# It starts at boot and after a crash. It does NOT restart on exit codes 2/3 (needs-you / spend-cap): those mean a human must act.
# Stop a manual run first (pkill -f run_pipeline): two drivers on one batch would collide.
# Logs: journalctl -u glossary -f   |   run.log in the repo root   |   bash deploy/status.sh
# Control: sudo systemctl stop|start|restart glossary
set -euo pipefail
BATCH="${1:?usage: install_service.sh batches/<batch_id>}"
: "${SNS_TOPIC_ARN:?export SNS_TOPIC_ARN first}"
REPO="$(pwd)"; ME="$(whoami)"

sudo tee /etc/glossary.env >/dev/null <<EOF
AWS_REGION=${AWS_REGION:-us-east-1}
MAX_USD=${MAX_USD:-300}
SNS_TOPIC_ARN=${SNS_TOPIC_ARN}
DRIVER_ARGS=${DRIVER_ARGS:---no-push}
EOF

sudo tee /etc/systemd/system/glossary.service >/dev/null <<EOF
[Unit]
Description=Glossary pipeline supervisor
After=network-online.target
Wants=network-online.target

[Service]
User=${ME}
WorkingDirectory=${REPO}
EnvironmentFile=/etc/glossary.env
ExecStart=${HOME}/env/bin/python ${REPO}/deploy/supervisor.py ${BATCH}
Restart=on-failure
RestartSec=60
RestartPreventExitStatus=2 3

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now glossary
sleep 2
sudo systemctl --no-pager status glossary | head -8
