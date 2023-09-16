terraform {
  backend "s3" {
    bucket = "terraform-backend"
    key    = "availability-checker/terraform.tfstate"
    region = "eu-west-1"
  }
}

provider "aws" {
  region = "eu-west-1"
}

resource "aws_s3_bucket" "lambda_code_bucket" {
  bucket = "daithi-code-bucket"
  acl    = "private"
}

resource "aws_s3_bucket_object" "lambda_code" {
  bucket = aws_s3_bucket.lambda_code_bucket.bucket
  key    = "availability_checker.zip"
  source = "../availability_checker.zip"
  etag   = filemd5("../availability_checker.zip")

  depends_on = [aws_s3_bucket.lambda_code_bucket]
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

resource "aws_lambda_function" "availability_checker" {
  function_name = "availability_checker"
  handler       = "app.main.handler"
  runtime       = "python3.11"

  role = aws_iam_role.lambda_role.arn

  # Zip should already be uploaded to S3
  s3_bucket = aws_s3_bucket.lambda_code_bucket.bucket
  s3_key    = aws_s3_bucket_object.lambda_code.key
}

resource "aws_cloudwatch_event_rule" "daily_run" {
  name                = "run-daily"
  description         = "Run Lambda function daily"
  schedule_expression = "rate(1 day)"
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
