JOB_NAME="ml-job-$(date +%Y%m%d%H%M%S)"  # Generate the job name using the current timestamp
sed "s/JOB_NAME_PLACEHOLDER/$JOB_NAME/" templates/ml-job-template.yaml > config_files/ml-job.yaml
# Verify the output
if [ -f "config_files/ml-job.yaml" ]; then
    echo "ml-job.yaml created successfully:"
    cat ml-job.yaml
else
    echo "Failed to create ml-job.yaml"
fi
