# BUS_445_termproject
Social Network Analysis of AI Adoption in High-Tech Managers.

## Group Members
* Tristan Brock
* Vincent Horn
* Andrew Garcia
* John Juste

## Project Overview
This project applies Social Network Analysis (SNA) to the Krackhardt High-Tech dataset to analyze how managerial network centrality and community structures correlate with organizational AI adoption sentiment.

## Repository Structure
* `code_for_anaylyzing_dataset.py` - The main Python script that builds the network, computes SNA metrics, and runs the simulation.
* `Krackhardt-High-Tech-main.zip` - The raw organizational dataset containing nodes, layers, and multiplex edges.
* `requirements.txt` - Python dependencies required to run the project.

## Setup & Execution
1. Ensure Python is installed on your machine.
2. Install the required dependencies by running:
   ```bash
   pip install -r requirements.txt


## Analytical Methodology

Our project uses Python and NetworkX to analyze
the organizational advice network in the
Krackhardt High-Tech Managers Dataset.

We will examine four main network metrics:

1. Network Density: Measures how connected
   the overall network is.
2. Degree Centrality: Identifies managers
   with the most direct connections.
3. Betweenness Centrality: Identifies managers
   who connect different parts of the organization.
4. Community Structure: Helps identify groups
   of managers who are more closely connected.

These metrics will help us identify influential
managers and examine how organizational
relationships could support AI adoption.
Since the original dataset does not measure
AI adoption directly, adoption status and
sentiment will be simulated for the project.
