#!/usr/bin/env python
"""
Script to download contents from a ftp server directory to local directory
"""
# Pylint & Flake8 configs
# pylint: disable=logging-fstring-interpolation
# pylint: disable=broad-exception-caught
# pylint: disable=line-too-long
# flake8: noqa: E501
import ftplib
import os
import logging
import argparse
import pathlib
import sys


# --- Configuration ---
FTP_HOST = '192.168.1.9'
FTP_PORT = 2121
FTP_USER = 'admin'
FTP_PASS = 'sample123'
REMOTE_DIR_TO_DOWNLOAD = 'Download/HdfcDoc'
LOCAL_DESTINATION_DIR = '/Users/jojijohny/Downloads/redmi/contacts'


# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("--loglevel", default="info",
                    help="Set log level \
                        (debug, info, warning, error, critical)"
                    )
args = parser.parse_args()

# Logging configurtion
script_filename = pathlib.Path(__file__).stem
logging.basicConfig(
    level=args.loglevel.upper(),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(script_filename)
logger.info("Starting Script: %s", pathlib.Path(__file__).name)


def download_from_ftp(ftp, remote_dir, local_dir):
    """ Downloads files and directories from ftp. """
    original_cwd = ftp.pwd()

    # Change to the remote directory if not already there
    logger.debug(f"Current working directory in ftp is: {original_cwd} and remote dir is: {remote_dir}")
    if original_cwd != remote_dir:
        try:
            ftp.cwd(remote_dir)
            logger.debug(f"Switching directory from {original_cwd} to {remote_dir}")
        except ftplib.error_perm as e:
            logger.error("Failed to change FTP directory to '%s': %s", remote_dir, e)
            ftp.cwd(original_cwd) # Revert CWD before exiting
            return

    # Create the local directory if it doesn't exist
    if not os.path.exists(local_dir):
        try:
            os.makedirs(local_dir)
            logger.info(f"Created local directory: {local_dir}")
        except OSError as e:
            logger.error("Failed to create local directory '%s': %s", local_dir, e)
            ftp.cwd(original_cwd)
            return


    # Get a list of items in the current remote directory
    try:
        items = ftp.nlst()
        logger.info("There are %d items in the directory: %s", len(items), remote_dir)
    except ftplib.error_perm as e:
        logger.error("Permission denied or error listing contents of '%s': %s", ftp.pwd(), e)
        ftp.cwd(original_cwd) # Revert CWD before exiting
        return

    # for item in items:
    #     # Construct full remote path for item
    #     remote_item_full_path = f"{remote_dir}/{item}"
    #     local_item_full_path = os.path.join(local_dir, item)
    #     logger.debug(f"remote_path: {remote_item_full_path} & local_path: {local_item_full_path}")
    #     try:
    #         # Check if item is a directory.
    #         current_remote_dir = ftp.pwd()

    #         try:
    #             ftp.cwd(item)
    #             logger.debug(f"Checking on directory: {item}")
    #             # Recurse into downloading the directory
    #             download_from_ftp(ftp, os.path.join('/', remote_item_full_path), local_item_full_path)
    #             logger.debug(f"Processed directory: {item}")
    #             # Going back direcotry where items were listed
    #             ftp.cwd(current_remote_dir)
    #         except ftplib.error_perm:
    #             # Checking if item is most likely a file
    #             logger.debug(f"Failed to process {item} as a directory. Hence attempting to download as file.")
    #             try:
    #                 with open(local_item_full_path, 'wb') as f:
    #                     logger.info(f"Downloading file: {item} to {local_item_full_path}")
    #                     ftp.retrbinary(f"RETR {item}", f.write)
    #             except Exception as e:
    #                 logger.error(f"Error downloading {item}: {e}")
    #         except Exception as e:
    #             logger.error(f"Unexpected error processing {item}: {e}",
    #                          exc_info=True)
    #     except Exception as e:
    #         logger.error(f"Unexpected error processing {item}: {e}")

    for item in items:
        # Check for potential empty item names
        if not item:
            logger.warning("Skipping empty item name in directory: %s", ftp.pwd())
            continue

        # Construct full remote path for item to pass to recursive calls (e.g., 'Documents/Tt1')
        # This 'remote_item_full_path' will be the argument 'remote_dir' in the next recursive call.
        current_ftp_abs_path = ftp.pwd() # Get current absolute path on FTP
        remote_item_full_path_for_next_call = os.path.join(current_ftp_abs_path, item).replace('\\', '/') # Ensure forward slashes for FTP paths

        local_item_full_path = os.path.join(local_dir, item)
        logger.debug("remote_path: %s & local_path: %s", remote_item_full_path_for_next_call, local_item_full_path)

        try:
            # Check if item is a directory by trying to cwd into it
            # Save current CWD before checking
            temp_cwd_for_check = ftp.pwd()
            is_directory = False
            try:
                ftp.cwd(item)
                is_directory = True
                logger.debug("Checking on directory: %s (is a directory)", item)
                ftp.cwd(temp_cwd_for_check) # Go back to the parent directory after checking
            except ftplib.error_perm:
                # If cwd fails, it's not a directory (likely a file)
                is_directory = False
                logger.debug("Failed to process %s as a directory. Attempting to download as file.", item)
            except Exception as e:
                logger.error("Unexpected error checking type of item %s: %s", item, e)
                continue # Skip this item if type check fails

            if is_directory:
                logger.info("Recursing into remote directory: %s", item)
                # Recurse: pass the FTP object, the relative item name, and the local path for the new directory
                # The recursive function will handle its own CWD logic.
                download_from_ftp(ftp, remote_item_full_path_for_next_call, local_item_full_path)
                logger.debug("Processed directory: %s", item)
                # The CWD is already restored by the recursive call's final ftp.cwd(original_cwd)
            else:
                # It's a file, download it
                remote_file_size = -1 # Default to unknown size
                try:
                    remote_file_size = ftp.size(item)
                    logger.debug("Remote file %s has size: %s bytes", item, remote_file_size)
                except Exception:
                    logger.debug("Could not get size for remote file %s", item)

                if os.path.exists(local_item_full_path):
                    local_file_size = os.path.getsize(local_item_full_path)
                    if remote_file_size != -1 and local_file_size == remote_file_size:
                        # Skip download, move to next item
                        logger.debug(f"Local file {local_item_full_path} already exists and sizes match ({local_file_size} bytes). Skipping download.")
                        continue

                try:
                    with open(local_item_full_path, 'wb') as f:
                        logger.debug("Downloading file: %s to %s", item, local_item_full_path)
                        ftp.retrbinary(f"RETR {item}", f.write)

                    # Verify downloaded file size
                    downloaded_size = os.path.getsize(local_item_full_path)
                    if downloaded_size == 0 and remote_file_size > 0:
                        logger.warning("Downloaded %s as 0 bytes, but remote size was %s bytes. Potential transfer issue.", item, remote_file_size)
                    elif downloaded_size != remote_file_size and remote_file_size != -1:
                        logger.warning("Downloaded %s size (%s bytes) does not match remote size (%s bytes).", item, downloaded_size, remote_file_size)
                    else:
                        logger.debug("Successfully downloaded %s (%s bytes)", item, downloaded_size)

                except ftplib.error_perm as e:
                    logger.error("Permission denied for downloading file %s: %s", item, e)
                except ftplib.error_temp as e:
                    logger.error("Temporary error during download of %s: %s", item, e)
                except ftplib.error_proto as e:
                    logger.error("Protocol error during download of %s: %s", item, e)
                except OSError as e: # Catch local file system errors
                    logger.error("Local file system error when writing %s: %s", local_item_full_path, e)
                except Exception as e:
                    logger.error("An unexpected error occurred during download of %s: %s", item, e)
        except Exception as e:
            logger.error("An unexpected error occurred while processing item %s: %s", item, e)
    logger.info(f"Completed downloads of files and directories under ftp directory: {remote_dir}")
    ftp.cwd(original_cwd)


def main():
    """ Main function. """
    logger.info("Initiating connection to ftp service.")
    try:
        ftp = ftplib.FTP()
        ftp.connect(FTP_HOST, FTP_PORT, timeout=300)
        ftp.login(user=FTP_USER, passwd=FTP_PASS)
        logger.info("Connected successfully to ftp service.")
    except (ftplib.error_reply, ftplib.error_temp, ftplib.error_perm,
            ftplib.error_proto, TimeoutError, OSError) as e:
        print(type(e))
        logger.error("Ftp connection failed: %s", e, exc_info=True)
        return
    download_from_ftp(ftp, REMOTE_DIR_TO_DOWNLOAD, LOCAL_DESTINATION_DIR)
    ftp.quit()
    logger.info("FTP connection closed.")


if __name__ == "__main__":
    main()
