import urllib.request
import zipfile
import os
import subprocess


def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)


def download_file(url, save_path):
    create_dir(os.path.dirname(save_path))

    try:
        with urllib.request.urlopen(url) as response:
            file_size = int(response.headers.get("Content-Length", 0))
            downloaded_bytes = 0
            with open(save_path, 'wb') as f:
                while True:
                    chunk = response.read(1024)  # Read 1KB at a time
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded_bytes += len(chunk)
                    progress = (downloaded_bytes / file_size) * 100
                    print(f"Downloading... {downloaded_bytes}/{file_size} bytes ({progress:.2f}%)", end='\r')
        print(f"\nFile downloaded successfully and saved at {save_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def bring_depot_tools():
    depot_tools_dir = os.path.abspath("./depot_tools")
    if not os.path.exists(depot_tools_dir):
        print("Fetching depot tools...", end="")
        file_path, _ = urllib.request.urlretrieve("https://storage.googleapis.com/chrome-infra/depot_tools.zip")
        print("Done")

        print("Extracting depot tools...", end="")
        depot_tools_zip = zipfile.ZipFile(file_path, 'r')
        depot_tools_zip.extractall(depot_tools_dir)
        print("Done")
    else:
        print("Found depot existing tools at " + depot_tools_dir)

    if not os.path.exists(f"{depot_tools_dir}/python3.bat"):
        print("Bootstrapping depot tools...", end="")
        subprocess.run([f"{depot_tools_dir}/update_depot_tools.bat"], check=True)
    else:
        print(f"Found python at {depot_tools_dir}/python3.bat")

    return depot_tools_dir


def bring_automate_script():
    automate_path = os.path.abspath(f"./automate/automate-git.py")

    if not os.path.exists(automate_path):
        print("Downloading automate.py")
        download_file(
            "https://raw.githubusercontent.com/chromiumembedded/cef/master/tools/automate/automate-git.py",
            automate_path)
    else:
        print(f"Found automate.py at {automate_path}")

    return automate_path


def main():
    depot_tools_path = bring_depot_tools()
    automate_path = bring_automate_script()


if __name__ == '__main__':
    main()
