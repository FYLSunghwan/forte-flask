import subprocess

def audiveris(input_path, output_path):
    subprocess.call(["sudo","docker","run","--rm",\
                     "-v", output_path+":/output",
                     "-v", input_path+":/input",\
                     "toprock/audiveris"])