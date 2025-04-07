# Research Collaborator Finder

The **Research Collaborator Finder** is a Python-based application designed to help users find research collaborators based on their project needs. It uses a database of researchers, advanced matching algorithms, and a chatbot interface to provide recommendations.

## Features

- **Researcher Database**: Stores researcher profiles with details like expertise, publications, and availability.
- **Dynamic Data Management**: Load, save, and update researcher data using a JSON file.
- **Sample Data Fallback**: Automatically loads sample data if no JSON file is available.
- **Extensible Design**: Easily add new researchers or integrate additional features.

## Researcher Database Overview

The `ResearcherDatabase` class is responsible for managing researcher data. Key features include:

1. **Loading Researchers**:
   - Loads researcher data from a JSON file (`app/data/researchers.json`).
   - Falls back to sample data if the file does not exist or an error occurs.

2. **Saving Researchers**:
   - Saves the current list of researchers to the JSON file, ensuring persistence.

3. **Adding Researchers**:
   - Dynamically adds new researchers to the database and updates the JSON file.

4. **Sample Data**:
   - Provides predefined sample researchers for testing and fallback purposes.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/research_collaborator_finder.git
   cd research_collaborator_finder