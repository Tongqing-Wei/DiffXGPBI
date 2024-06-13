# DiffXGPBI

### a machine learning method for prediction of phage-bacterial interactions based on difference vectors

## Installion

##### 1. Create Conda environment

By creating a Conda environment, you can have separate environments for different projects or purposes, ensuring that the packages and dependencies within each environment do not conflict with each other.

```shell
conda create -n DiffXGPBI python=3.9
```

##### 2. Activate your Conda environment

Once the environment is created, you can activate it and start installing packages or running programs within that environment, ensuring that the installed packages and dependencies are isolated from your system's global environment.

```shell
conda activate DiffXGPBI
```

##### 3. Install prokka and blast using the Conda package manager

To install the prokka as a dependency, once the installation is finished, you can start using prokka and blast within your Conda environment.

```shell
conda install biobuilds::prokka
# If the installation is successful, the script below should run without any issues
prokka -h
# set database index for prokka
prokka --setupdb

```

##### 4. Install python modules using pip

Any of the python third-party libraries involved can be installed by pip (pip install *), where torch is installed using the following command. Refer to requirements. 

```shell
pip install xgboost
```

## DiffXGPBI main workflow

##### 1. Prokka annotation 

Run ***prokka.sh*** to get a batch of prokka annotation files. Input the fasta files of some phages (bacterium) under a folder, and output a prokka annotation folder for each phage (bacteria). 

```shell
Usage:
  bash prokka.sh [-i <FASTA_FOLDER>] [-o <OUTPUT_FOLDER>] [-p <PROKKA_PATH>]
  -i FASTA_FOLDER	Input folders (some fasta files containing phages or bacteria)
  -o OUTPUT_FOLDER	Output folders (annotation result folder for each phage or bacteria generated by annotations)
  -p PROKKA_PATH	Prokka software script location path
  
Example:
  bash prokka.sh -i ./example_phage -o ./example_phage_annotation -p ~/.conda/envs/DiffXGPBI/bin/prokka 
  
  bash prokka.sh -i ./example_host -o ./example_host_annotation -p ~/.conda/envs/DiffXGPBI/bin/prokka
```

##### 2. Predictive result

Run ***DiffXGPBI.py*** to predict PBI and directly generate prediction results. Example of prediction results: 

- ***Phage*** is the phage ID to be predicted. 
- ***Bacterium*** is the bacterium ID to be predicted. 
- ***output*** is the prediction result of whole genome model. 

```shell
Usage:
  python DiffXGPBI.py [--phage_annotation <PHAGE_FOLDER>] [--bacterium_annotation <BACTERIUM_FOLDER>] [--output <OUTPUT_RESULT>] [--model <MODEL_PARAMETER>] [--template <INTERMEDIATE_RESULT>] 
  --phage_annotation PHAGE_FOLDER	Phage folder after annotation
  --bacterium_annotation BACTERIUM_FOLDER	Bacteria folder after annotation
  --output OUTPUT_RESULT	Predict result output path
  --model MODEL_PARAMETER	Related model parameter files, including model parameters and key genes list, as well as standardized scaler pkl files for input features
  --template INTERMEDIATE_RESULT	A temporary folder to store intermediate results
	
Example:
  python DiffXGPBI.py --phage_annotation ./example_phage_annotation --bacterium_annotation ./example_host_annotation --output ./example_output --model ./model --template ./template
```

## File description

| File name                | Description                                                  |
| ------------------------ | ------------------------------------------------------------ |
| case                     | case fasta data                                              |
| code                     | data process and intermediate result analysis code           |
| example_host             | sample host fasta folder                                     |
| example_host_annotation  | sample host's prokka annotation result folder                |
| example_output           | example output result csv  file and html file                |
| example_phage            | sample phage fasta folder                                    |
| example_phage_annotation | sample phage's prokka annotation result folder               |
| host_external            | the fasta sequence file of bacteria in external validation dataset |
| host_raw_data            | the fasta sequence file of bacteria in our collected raw dataset |
| model                    | modle parameter related file                                 |
| phage_external           | the fasta sequence file of phage in our collected raw dataset |
| phage_raw_data           | the fasta sequence file of phage in our collected raw dataset |
| template                 | intermediate generated feature result file                   |
| DiffXGPBI.py             | DiffXGPBI model predict code                                 |
| prokka.sh                | prokka annotation code                                       |
| requirements.txt         | run DeepPBI-KG required related python module                |
| ReadMe.md                | ReadMe Markdown                                              |

