import subprocess
import os, shutil, click

@click.command()
@click.option("--folder", default="../../../data/mc4/0_raw", help="Destination folder where to write")
@click.option("--temp", default="../../../_temp", help="Temporary folder used to extract archives")
@click.option("--overwrite", is_flag=True, help="Clean and start from scratch")

def main(folder, temp, overwrite):
    folder = os.path.abspath(folder)
    temp = os.path.abspath(temp)

    print("Install git-lfs")
    subprocess.run(['sudo', 'apt', 'install', 'git-lfs'])

    print("Clone the repository")
    subprocess.run(['git', 'clone', 'https://huggingface.co/datasets/allenai/c4'])

    print("Change directory to c4")
    os.chdir('c4')

    print("Set GIT_LFS_SKIP_SMUDGE=1 environment variable")
    os.environ['GIT_LFS_SKIP_SMUDGE'] = '1'

    print("Pull LFS files")
    subprocess.run(['git', 'lfs', 'pull', '--include', 'multilingual/c4-ro.*.json.gz'])

    print("Go back to the previous directory")
    os.chdir('..')

    if overwrite:
        print(f"==== [ OVERWRITING ] ====")

    if os.path.exists(folder):
        if not overwrite:
            print(f"\nFolder {folder} already exists, not doing anything.\n")
            #return
        else:  
            print("Cleanup...")
            shutil.rmtree(folder, ignore_errors=True)
            shutil.rmtree(temp, ignore_errors=True)

    os.makedirs(folder, exist_ok=True)
    os.makedirs(temp, exist_ok=True)

    print("Downloading MC4 dataset...")
    subprocess.run(['python3', 'c4_extractor.py', '--data_dir', temp, '--output_dir', folder])
    
    print("Cleaning the c4 repo...")
    subprocess.run(['sudo', 'rm', '-r', 'c4'])

if __name__ == "__main__":
    main()
