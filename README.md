# AI Lab Coursework

This repository contains the solutions and experimental code for the AI Laboratory coursework, structured across four distinct modules:

## Directory Structure

1. **Neural_network_lab/**
   * Implements a 2-layer Neural Network (using PyTorch) to solve the binary XOR problem and a 3-class extension.
   * Investigates the effects of different non-linear activation functions (Sigmoid, Tanh, ReLU) and symmetric weight initialization.
   * Contains the execution script, generated loss/activation plots, and a comprehensive lab report (`neural_network_lab_report.md`).

2. **Agents_lab/**
   * Explores the design of a goal-based agent navigating a 2D warehouse environment to transport packages.
   * Contains a pure Python implementation of the agent using BFS to find optimal collision-free paths.
   * Includes the lab report (`agents_lab_report.md`) detailing the agent's architecture, problem formulation, and state tracking.

3. **Search_lab/**
   * Formulates the warehouse navigation problem as a mathematical search problem.
   * Compares the performance (path length, nodes expanded) of unguided Breadth-First Search (BFS) against heuristically-guided A* search.
   * Investigates the properties of different distance heuristics (Manhattan vs. Euclidean) and admissibility. 
   * Includes the search implementation and the lab report (`search_lab_report.md`).

4. **Logic_lab/**
   * Uses Logical Reasoning to implement a logical planner for a warehouse robot with pickup/drop capabilities.
   * Verifies action applicability and simulates state transitions based on propositional logic preconditions and effects.
   * Includes an independent logical verifier written in Prolog (`planner.pl`) to mathematically prove the planner's output.
   * Includes the planner implementation and the lab report (`logic_lab_report.md`).
