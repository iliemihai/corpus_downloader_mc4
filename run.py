import subprocess
import os, shutil, click

@click.command()
@click.option("--folder", default="./data/", help="Destination folder where to write")
@click.option("--temp", default="./temp", help="Temporary folder used to extract archives")

def main(folder, temp):
    folder = os.path.abspath(folder)
    temp = os.path.abspath(temp)

    print("Install git-lfs")
    subprocess.run(['sudo', 'apt', 'install', 'git-lfs'])

    print("Set GIT_LFS_SKIP_SMUDGE=1 environment variable")
    os.environ['GIT_LFS_SKIP_SMUDGE'] = '1'

    print("Clone the repository")
    subprocess.run(['git', 'clone', 'https://huggingface.co/datasets/allenai/c4'])

    print("Change directory to c4")
    os.chdir('c4')

    #print("Set GIT_LFS_SKIP_SMUDGE=1 environment variable")
    #os.environ['GIT_LFS_SKIP_SMUDGE'] = '1'

    print("Pull LFS files")
    subprocess.run(['git', 'lfs', 'pull', '--include', 'multilingual/c4-ro.*.json.gz'])
    subprocess.run('mv', 'multilingual/c4-ro.*.json.gz', temp)

    print("Go back to the previous directory")
    os.chdir('..')

    os.makedirs(folder, exist_ok=True)
    os.makedirs(temp, exist_ok=True)

    print("Extract MC4 dataset...")
    subprocess.run(['python3', 'c4_extractor.py', '--data_dir', temp, '--output_dir', folder])
    
    print("Cleaning the c4 repo...")
    subprocess.run(['sudo', 'rm', '-r', 'c4'])

if __name__ == "__main__":
    main()
