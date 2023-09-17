# Availability Checker app
AWS Lambda function triggered on a Cloudwatch event timer and publishes results to SNS Topic

### First time setup

Requires AWS CLI to be installed and configured locally with credentials:

- Run `aws configure` and follow the prompts to add AWS Secrets and region `eu-west-1`

### Run Locally

Run `python app/main.py` in the terminal

### Run unittests

Run `python -m pytest -v` in the terminal

### Create Lambda build

1. Use `mkdir build` to create build directory

2. Install bs4 into the build directory (as it is not available on Lambda):
   `pip install beautifulsoup4 -t build/`

3. Package app code:
    ```
    cp -r app/* build/
    cd build
    zip -r ../availability_checker.zip .
    ```

    OR on Windows: 

   ```
   xcopy app\* build\ /E /I
   cd build
   powershell Compress-Archive -Path * -DestinationPath ..\availability_checker.zip
   ```


### TODOs

 - Use S3 bucket for the search_urls.txt
 - Async process urls
