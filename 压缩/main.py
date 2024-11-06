import os, tarfile
from datetime import datetime
import uuid
from tokenize import endpats

from sqlalchemy.sql.functions import random


def create_tar_xz(dst_dir: str = None, src_dir: str = None):
    if dst_dir is None:
        dst_dir = os.path.join(os.getcwd(), str(uuid.uuid4()) + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".tar.xz")
    if "tar.xz" not in dst_dir:
        dst_dir += ".tar.xz"

    if src_dir is None:
        src_dir = os.getcwd()
        print(src_dir)
    with tarfile.open(dst_dir, "w:xz",encoding='utf-8') as tar:
        for x in os.listdir(src_dir):
            if x == "main.py" or x == src_dir:
                continue
            print("search file: " + x)
            tar.add(x, arcname=os.path.basename(x))

    print("Compressed successfully")


create_tar_xz()
