JOB_NAME="ml-job-$(date +%Y%m%d%H%M%S)"  # Generate the job name using the current timestamp
sed "s/JOB_NAME_PLACEHOLDER/$JOB_NAME/" templates/ml-job-template.yaml > config_files/ml-job.yaml

