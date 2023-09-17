terraform {
  backend "s3" {
    bucket = "daithi-terraform-backend"
    key    = "availability-checker/terraform.tfstate"
    region = "eu-west-1"
  }
}

provider "aws" {
  region = "eu-west-1"
}

resource "aws_sns_topic" "product_alert" {
  name = "product-alert"
}

resource "aws_sns_topic_subscription" "product_alert_email" {
  topic_arn = aws_sns_topic.product_alert.arn
  protocol  = "email"
  endpoint  = "daithi@hotmail.co.uk"
}

data  "aws_iam_policy_document" "sns_publish" {
  statement {
    actions   = ["sns:Publish"]
    resources = [aws_sns_topic.product_alert.arn]
  }
}

resource "aws_iam_policy" "sns_publish_policy" {
  name        = "LambdaSNSTopicPublish"
  description = "Allows Lambda to publish to SNS topics"
  policy      = data.aws_iam_policy_document.sns_publish.json
}

resource "aws_iam_role" "lambda_role" {
  name = "availability-checker-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
        Effect = "Allow"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_sns_publish_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.sns_publish_policy.arn
}

resource "aws_lambda_function" "availability_checker" {
  filename      = "${path.module}/../availability_checker.zip"
  function_name = "availability_checker"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.handler"

  runtime       = "python3.11"
  timeout       = 30

  environment {
    variables = {
      PRODUCT_ALERT_TOPIC_ARN = aws_sns_topic.product_alert.arn
    }
  }
}

resource "aws_cloudwatch_event_rule" "daily_run" {
  name                = "run-daily"
  description         = "Run Lambda function daily"
  schedule_expression = "rate(1 day)"

  is_enabled = false  # Disabled for now
}

resource "aws_cloudwatch_event_target" "check_availability" {
  rule      = aws_cloudwatch_event_rule.daily_run.name
  target_id = "availabilityChecker"
  arn       = aws_lambda_function.availability_checker.arn
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowCloudWatchEventsInvocation"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.availability_checker.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily_run.arn
}
