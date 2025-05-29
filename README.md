# PrepX - Tech Interview MCQ Development System

PrepX is a Streamlit application that leverages the Google Gemini API to generate multiple-choice questions (MCQs) for technical interviews. It allows users to specify disciplines, systems, competencies, and keywords to tailor the generated questions.

## Features

* **Generate MCQs:** Create customized MCQs based on user-defined criteria.
* **Multiple Disciplines, Systems, and Competencies:** Select multiple options from predefined lists.
* **Keyword Input:** Add specific keywords to focus the questions.
* **Number of Questions:** Set the number of MCQs to generate.
* **Direct Display:** Displays the generated questions directly in the Streamlit app.
* **Environment Variable Security:** Uses a `.env` file to securely store your Gemini API key.

## Prerequisites

* Python 3.6+
* Streamlit (`pip install streamlit`)
* Google Generative AI (`pip install google-generai`)
* python-dotenv (`pip install python-dotenv`)
* Google Gemini API Key

## Setup

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install dependencies:**
    ```bash
    pip install streamlit google-generai python-dotenv
    ```

3.  **Create a `.env` file:**
    * In the root directory of the project, create a file named `.env`.
    * Add your Gemini API key to the `.env` file:
        ```
        GEMINI_API_KEY="YOUR_ACTUAL_API_KEY"
        ```
        Replace `"YOUR_ACTUAL_API_KEY"` with your actual API key.

4.  **Run the Streamlit application:**
    ```bash
    streamlit run PrepX.py
    ```

5.  **Access the application:**
    * Open your web browser and navigate to the URL displayed in the terminal (usually `http://localhost:8501`).

## Usage

1.  **Select Disciplines:** Choose one or more disciplines from the dropdown list.
2.  **Select Systems:** Choose one or more systems from the dropdown list.
3.  **Select Competencies:** Choose one or more competencies from the dropdown list.
4.  **Enter Keywords:** Enter any specific keywords you want to include in the questions.
5.  **Enter Number of Questions:** Enter the number of questions you would like to generate.
6.  **Click "Generate MCQs":** The application will generate the specified number of MCQs and display them on the page.


Feel free to contribute to this project by submitting pull requests or opening issues.

## License

This project is licensed under the terms of the MIT License. See the [LICENSE](LICENSE) file for details.
