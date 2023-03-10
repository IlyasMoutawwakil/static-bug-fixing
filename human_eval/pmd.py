import pandas as pd
from pathlib import Path
from subprocess import Popen, PIPE, SubprocessError
from typing import Tuple
import xml.etree.ElementTree as ET

PMD_CMD = "/home/ilyas/Desktop/Github/static-bug-fixing/pmd-bin-6.55.0/bin/run.sh pmd"
PMD_RULES_PATH = "/home/ilyas/Desktop/Github/static-bug-fixing/pmd-bin-6.55.0/custom_rules.xml"

def run_PMD(file_path: Path) -> Tuple[str, str]:
    """Run PMD on `file_path` in a subprocess and return stdout and stderr.

    :param file_path: path to the file on which PMD is run
    :type file_path: pathlib.Path
    :raises SubprocessError: when an error occurres when running PMD in a subprocess
    :raises UnicodeError: when the stdout and stderr of the subprocess cannot be decoded into UTF-8
    :rtype: (str, str)
    """
    cmd = f"{PMD_CMD} -d {file_path} -R {PMD_RULES_PATH} -f xml"
    pmd_output = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    pmd_stdout, pmd_stderr = pmd_output.communicate()
    return pmd_stdout.decode(), pmd_stderr.decode()

def get_PMD_xml_root(file_path: Path) -> ET.Element:
    """Get the root element of PMD XML output on `file_path`.

    :param file_path: path to the file on which PMD is run
    :type file_path: pathlib.Path
    :raises SubprocessError: when an error occurres when running PMD in a subprocess
    :raises UnicodeError: when the stdout and stderr of the subprocess cannot be decoded into UTF-8
    :raises RuntimeError: when PMD subprocess' stdout does not contain XML data
    :rtype: xml.etree.ElementTree.Element
    """
    
    try:
        pmd_stdout, pmd_stderr = run_PMD(file_path)
    except (SubprocessError, UnicodeError):
        raise
    xml_start = pmd_stdout.find("<?xml")
    if xml_start == -1:
        raise RuntimeError(f"No XML tag in PMD subprocess' stdout\nPMD subprocess' stderr:\n{pmd_stderr}")
    str_xml = pmd_stdout[xml_start:]
    root = ET.fromstring(str_xml)
    return root

def PMD_dataframe(file_path: Path) -> pd.DataFrame:
    """Run PMD on `file_path` in a subprocess and convert the XML output into a `pandas.DataFrame`. 
    An empty DataFrame is returned if no violations were detected.

    :param file_path: path to the file on which PMD is run
    :type file_path: pathlib.Path
    :raises SubprocessError: when an error occurres when running PMD in a subprocess
    :raises UnicodeError: when the stdout and stderr of the subprocess cannot be decoded into UTF-8
    :raises RuntimeError: when PMD subprocess' stdout does not contain XML data or the XML has an error tag
    :rtype: pandas.DataFrame
    """
    root = get_PMD_xml_root(file_path)
    if len(root) == 0: # root element has no children
        return pd.DataFrame() # empty DataFrame
    if root[0].tag == "error":
        raise RuntimeError(f"PMD XML output contains error tag: {root[0].attrib['msg']}")
    
    return pd.DataFrame([dict([*v.items(), ("message", v.text)]) for v in root[0]])