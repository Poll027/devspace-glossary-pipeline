#!/usr/bin/env bash
# Run in AWS CloudShell (or any shell with your IAM user's credentials), NOT on the pipeline instance:
#   bash aws_budget_alarms.sh you@example.com
# Creates (1) an SNS topic the driver notifies when it finishes or stops, and (2) a budget "glossary-bedrock"
# that emails you when ACTUAL spend passes $500, $700 and $1000.
# IncludeCredit=false so the budget tracks gross usage; with credits included, net spend stays $0 and nothing would ever fire.
# AWS Budgets only refreshes a few times a day, so the alarm can lag; the driver's own MAX_USD cap is the hard stop.
set -euo pipefail
EMAIL="${1:?usage: aws_budget_alarms.sh <email>}"
REGION=us-east-1
ACCOUNT=$(aws sts get-caller-identity --query Account --output text)

TOPIC=$(aws sns create-topic --name glossary-driver --region "$REGION" --query TopicArn --output text)
aws sns subscribe --topic-arn "$TOPIC" --protocol email --notification-endpoint "$EMAIL" --region "$REGION" >/dev/null
echo "SNS topic: $TOPIC (confirm the subscription email)"

cat > /tmp/budget.json <<JSON
{"BudgetName": "glossary-bedrock",
 "BudgetLimit": {"Amount": "1000", "Unit": "USD"},
 "TimeUnit": "MONTHLY", "BudgetType": "COST",
 "CostTypes": {"IncludeTax": true, "IncludeSubscription": true, "UseBlended": false, "IncludeRefund": false,
               "IncludeCredit": false, "IncludeUpfront": true, "IncludeRecurring": true, "IncludeOtherSubscription": true,
               "IncludeSupport": true, "IncludeDiscount": true, "UseAmortized": false}}
JSON

python3 - "$EMAIL" > /tmp/notifs.json <<'PY'
import json, sys
print(json.dumps([{"Notification": {"NotificationType": "ACTUAL", "ComparisonOperator": "GREATER_THAN", "Threshold": t, "ThresholdType": "ABSOLUTE_VALUE"},
                   "Subscribers": [{"SubscriptionType": "EMAIL", "Address": sys.argv[1]}]} for t in (500, 700, 1000)]))
PY

aws budgets create-budget --account-id "$ACCOUNT" --budget file:///tmp/budget.json --notifications-with-subscribers file:///tmp/notifs.json
echo "Budget created: alerts at \$500, \$700, \$1000 actual spend -> $EMAIL"
echo "Next: give the instance role 'sns:Publish' on $TOPIC, and set SNS_TOPIC_ARN=$TOPIC on the instance."
