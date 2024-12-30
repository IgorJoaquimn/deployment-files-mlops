JOB_NAME="ml-job-$(date +%Y%m%d%H%M%S)"  # Generate the job name using the current timestamp
sed "s/JOB_NAME_PLACEHOLDER/$JOB_NAME/" ml-job-template.yaml | kubectl apply -f -

