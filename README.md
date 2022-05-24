# Juji Python Client

Python client to Juji chatbot. Currently only text messages in chat are supported.

## Environemnt Set Up
1. Install [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
2. Install the conda environment
    ```console
    conda env create -f environment.yml
    ```

## Chat
1. Activate your python environment
    ```console
    conda activate juji-client
    ```
2. Run the program
    ```console
    python juji_chat.py <chatbot url> [--firstname <first name>] [--lastname <last name>] [--email <email>]
    ```
