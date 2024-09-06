import os
import yaml

def create_directory_structure():
    directories = [
        ".github/workflows",
        "notebook",
        "calories",
        "calories/components",
        "calories/entity",
        "calories/pipeline",
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        
    print("Directory structure created successfully.")

def create_files():
    files = {
        ".github/workflows/main.yaml": "",
        "notebook/test.ipynb": "",
        "calories/__init__.py": "# __init__py_content",
        "calories/config.py": "# config_py_content",
        "calories/exception.py": "# exception_py_content",
        "calories/logger.py": "# logger_py_content",
        "calories/predictor.py": "# predictor_py_content",
        "calories/utils.py": "# utils_py_content",
        "calories/components/__init__.py": "# components_init_py_content",
        "calories/components/data_ingestion.py": "# data_ingestion_py_content",
        "calories/components/data_transformation.py": "# data_transformation_py_content",
        "calories/components/data_validation.py": "# data_validation_py_content",
        "calories/components/model_evaluation.py": "# model_evaluation_py_content",
        "calories/components/model_trainer.py": "# model_trainer_py_content",
        "calories/components/model_pusher.py": "# model_pusher_py_content",
        "calories/entity/__init__.py": "# entity_init_py_content",
        "calories/entity/artifact_entity.py": "# artifact_entity_py_content",
        "calories/entity/config_entity.py": "# config_entity_py_content",
        "calories/pipeline/__init__.py": "# pipeline_init_py_content",
        "calories/pipeline/training_pipeline.py": "# training_pipeline_py_content",
        "calories/pipeline/prediction_pipeline.py": "# prediction_pipeline_py_content",
        ".gitignore": "# gitignore_content",
        "data_dump.py": "# data_dump_py_content",
        "Dockerfile": "# Dockerfile_content",
        "main.py": "# main_py_content",
        "README.md": "# readme_md_content",
        "requirements.txt": "# requirements_txt_content",
        "setup.py": "# setup_py_content",
        ".env": "# .env_content"
    }
    
    for file_path, content in files.items():
        with open(file_path, "w") as f:
            f.write(content)
        print(f"Created {file_path}")

if __name__ == "__main__":
    create_directory_structure()
    create_files()
    print("Project structure  created successfully.")

