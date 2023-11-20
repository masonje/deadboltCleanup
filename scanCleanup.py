import os
import logging

def delete_file(file_path):
    """
    Delete a file.

    Parameters:
        file_path (str): Path to the file to be deleted.
    """
    try:
        os.remove(file_path)
        logger.info(f"File '{file_path}' successfully deleted.")
    except FileNotFoundError:
        logger.warn(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(f"An error occurred: {e}")

def write_to_file(file_path, content):
    try:
        with open(file_path, 'a') as file:
            file.write(content + '\n')
        print(f"Content successfully written to {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def setup_logging(log_file_path='app.log', log_level=logging.INFO):
    """
    Set up logging configuration.

    Parameters:
        log_file_path (str): Path to the log file.
        log_level (int): Logging level (default is INFO).

    Returns:
        logging.Logger: Configured logger.
    """
    # Create the log directory if it doesn't exist
    log_directory = os.path.dirname(log_file_path)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Create a logger and set the level
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Create a file handler and add it to the logger
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Create a console handler and add it to the logger
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

def list_all_files_and_folders(directory):
    result = []
    
    def recursive_list(current_directory):
        try:
            with os.scandir(current_directory) as entries:
                for entry in entries:
                    result.append(entry.path)
                    if entry.is_dir():
                        recursive_list(entry.path)
        except FileNotFoundError:
            print(f"The specified directory '{current_directory}' was not found.")

    # Start the recursive listing
    recursive_list(directory)
    return result

if __name__ == "__main__":
    directory_path = "/run/user/1000/gvfs/smb-share:server=nas.local,share=pictures/2021"

    bext='.deadbolt'
    list_deatlocks="logs/deadlocks.list"
    list_deadlocks_orphen="logs/deadlocks_orphen.list"
    list_nodeadlock="logs/nodeadlock.list"

    log_file_path = "logs/deadboltCleanup.log"
    logger = setup_logging(log_file_path)

    logger.info("----------------------------------")
    logger.info("Scanning: " + directory_path)
    result_list = list_all_files_and_folders(directory_path)
    result_size=len(result_list)
    logger.info("Scan complete. Returned items: " + str(result_size))

    for item in result_list:
        logger.debug("File: " + item)
        if os.path.isdir(item):
            logger.debug("Skipping folder " + item)
        else:
            fsplit = os.path.splitext(item)
            fname = fsplit[0]
            fext = fsplit[1]
            if fext == bext:
                logger.debug("Deadlock file found: " + item)
                if os.path.isfile(fname):
                    # deaslock and file exist. Check file enrypted status.
                    logger.info("Deadlock and source for: " + fname)
                    write_to_file(list_deatlocks, fname)

                    # Delete deadlock?
                else:
                    logger.warn("Orphen Deadlock: " + item)
                    write_to_file(list_deadlocks_orphen, item)
            else:
                logger.debug("Non-"+bext+" extention: " + fext)

                #checking for deadbolt and regular file equivlent 
                logger.debug("Checking for: " + item + bext)
                if os.path.isfile(item + bext):
                    logger.warn("Deadbolt file found for: " + item)
                    write_to_file(list_nodeadlock, item + bext)
                    # Delete deadbold file
                    delete_file(item)
                else:
                    logging.WARN("Deadbolt file NOT found for: " + item)
                    write_to_file(list_nodeadlock, item)




