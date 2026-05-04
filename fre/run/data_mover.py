# fre run data_mover.py subtool
import fre_run_init.py #placeholder for future global variables import

import pandas
import os
import shutil
import subprocess
from pathlib import Path

# ---------------- save restart files, namelist, tables etc. and move them from RESTART to INPUT
# Needs to inherete: workDir, patternGrepRestart, enddate, outputDir, tmpOutputDir, rtsxml, scriptName, prepareDir
# Save original directory
original_dir = os.getcwd()

try:
    # Change to RESTART directory
    os.chdir(f"{workDir}/RESTART")
    
    # Get restart files matching pattern
    result = subprocess.run(f"ls -1 | egrep '{patternGrepRestart}'", shell=True, capture_output=True, text=True)
    restart_files = [f for f in result.stdout.strip().split('\n') if f]
    
    if restart_files:
        restart_suffix = f"restart/{enddate}"
        restart_arch_dir = f"{outputDir}/{restart_suffix}"
        restart_work_dir = f"{tmpOutputDir}{restart_arch_dir}"
        
        # Prepare directory
        prepareDir(restart_work_dir, 'clean')
        
        # Create symbolic links for restart files
        for file in restart_files:
            src = os.path.join(os.getcwd(), file)
            dst = os.path.join(restart_work_dir, file)
            os.symlink(src, dst)
        
        # Copy files with preservation of mode, ownership, and timestamps
        shutil.copy2(f"{workDir}/input.nml", restart_work_dir)
        
        # Copy all _table files
        for file in Path(workDir).glob("*_table"):
            shutil.copy2(str(file), restart_work_dir)
        
        # Copy all _table.yaml files
        for file in Path(workDir).glob("*_table.yaml"):
            shutil.copy2(str(file), restart_work_dir)
        
        # Copy rtsxml and script files
        shutil.copy2(rtsxml, restart_work_dir)
        shutil.copy2(scriptName, restart_work_dir)

finally:
    # Return to original directory
    os.chdir(original_dir)
